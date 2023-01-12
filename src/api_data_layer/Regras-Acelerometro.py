from math import floor
import time
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from influxdb import InfluxDBClient
from datetime import datetime as dt

# Constants
GRAFANA_URL_SHIFT = 1200  # Shift the end of the time series by 20 min
GRAFANA_URL_SHIFT_LESS = 600  # Shift the start of the time series by 10 min
IOTAWATT_SAMPLE_TIME = 0.2
# QUERY_AMOUNT is about the max number of values(data points) needed to analize all the set of rules
# as of this code, the rule 4 have the most number of values (14)
QUERY_AMOUNT = 14


def main():
    last_ttsamp = 0
    rules = ['rule1', 'rule3', 'rule4', 'rule6']
    accel_fields = ['AccelX', 'AccelY', 'AccelZ']
    while True:
        # Holds the value if any rule was fired in any column
        alert_string_HTML = """\
            <html>
                <body>
            """
        alert_string_plain = ''
        rules_Fired = 0
        # Connecting to the influxDB
        client = InfluxDBClient(
            host='193.136.195.105', port=8086, username='admin', password='catraport2020')
        # Get the last queryAmount values from the whole Database and work on them
        # It may seems to be a lengthy query, but it's quicker than doing a SQL request for each column name
        client.switch_database('acelerometro')
        results = client.query(
            'SELECT AccelX,AccelY,AccelZ FROM Measures ORDER BY "time" DESC LIMIT '+str(QUERY_AMOUNT))
        this_time = list(results.get_points())[0]['time']
        # If the last timestamp recorded is equal to last queried time, do nothing
        if last_ttsamp == this_time:
            print('Same values, waiting for new values!')
        else:  # Otherwise Run...
            last_ttsamp = this_time
            # Get the last thousand values to do the mean and the standard deviation of each column
            result_aux = client.query(
                'SELECT PERCENTILE(*,10) as "Perc10",PERCENTILE(*,90) as "Perc90" FROM Measures')
            points = list(result_aux.get_points())
    # print(points)
            min_x, min_y, min_z = points[0]["Perc10_AccelX"], points[0]["Perc10_AccelY"], points[0]["Perc10_AccelZ"]
            max_x, max_y, max_z = points[0]["Perc90_AccelX"], points[0]["Perc90_AccelY"], points[0]["Perc90_AccelZ"]
    # print(points[0]["Perc25_AccelX"])
            where_txt = f'(AccelX<{min_x} or AccelX>{max_x}) and (AccelY<{min_y} or AccelY>{max_y}) and (AccelZ<{min_z} or AccelZ>{max_z})'
            results_analisys = client.query(
                f'SELECT stddev(AccelX),stddev(AccelY), stddev(AccelZ), mean(AccelX),mean(AccelY), mean(AccelZ) FROM Measures where {where_txt} ')
            #points = list(results_analisys.get_points())
            # Now for each column
            for accel_name in accel_fields:
                accel_name_helper = f'Aceleração eixo {accel_name[-1]}'
                # Filter the points by the measurement
                points = list(results.get_points())
                current_values = []
                tstamp = []
                # Turn them all into a list
                for point_index in range(QUERY_AMOUNT):
                    current_values.append(points[point_index][accel_name])
                    tstamp.append(points[point_index]['time'])
                    # If there is no new values being uploaded by the IoTaWatt to the influx, the last timestamp will be equal
                    # to the timestamp made by the query above (client.query)
                    # Filter the stddev and the mean by the measurement
                points_analisys = list(
                    results_analisys.get_points())
                aux = ''
                if accel_name == 'AccelY':
                    aux = '_1'
                elif accel_name == 'AccelZ':
                    aux = '_2'
                stddev = points_analisys[0][f'stddev{aux}']
                mean = points_analisys[0][f'mean{aux}']
                rules_fired_array = [0, 0, 0, 0]
                # For each chosen rule
                for rule in rules:
                    # Technically I could use only 1 counter, but I trust the Rasp power (4 cores...)
                    count_rule3, count_rule4, count_rule6 = 0, 0, 0
                    previous_was_bigger, previous_was_lower = True, True
                    first_value, first_rule1_detection = True, True
                    # For every queryAmount values
                    for value in current_values:

                        # ====================================================================================================
                        # RULE1
                        if (value > (mean+(3*stddev)) or value < (mean-(3*stddev))) and rule == 'rule1' and first_rule1_detection:
                            alert_string_HTML = alert_string_HTML + f"""\
                            <p> Um dos valores analisados está altamente fora de controle - {accel_name_helper}.</p>
                            """
                            alert_string_plain = alert_string_plain + \
                                f"""\nUm dos valores analisados está altamente fora de controle - {accel_name_helper}."""
                            print('rule1 Fired')
                            rules_fired_array[0] = 1
                            #write_database(client, 1, last_ttsamp)
                            rules_Fired = rules_Fired + 1
                            first_rule1_detection = False

                        # ====================================================================================================
                        # RULE 3
                        if (rule == 'rule3'):
                            # If is the first value to enter, there is nothing to compare, save it
                            if first_value:
                                # Could start it with 1 up there, but...
                                count_rule3 = 1
                                last_value = value
                                first_value = False
                            else:
                                if value > last_value:  # if the actual value is bigger than the last
                                    if previous_was_lower:  # and the previous was lower
                                        count_rule3 = count_rule3+1  # then there is a trend going up, add to the counter
                                        previous_was_bigger = False  # and, obviously the previous was not bigger
                                    else:
                                        previous_was_lower = True  # else, then the previous was lower
                                        count_rule3 = 1  # reset the counter to 1, to include this value

                                if value < last_value:  # use the same logic above...
                                    if previous_was_bigger:
                                        count_rule3 = count_rule3+1
                                        previous_was_lower = False
                                    else:
                                        previous_was_bigger = True
                                        count_rule3 = 1
                                last_value = value
                            # Six points(30s of variation) are going up or down
                            if count_rule3 == QUERY_AMOUNT:
                                count_rule3 = -QUERY_AMOUNT  # Reset to don't send more than 1 tome the same message
                                tendency = 'subida' if previous_was_lower else 'queda'
                                alert_string_HTML = alert_string_HTML + f"""\
                                <p>Existe uma tendência de {tendency} nos dados - {accel_name_helper}.</p>
                                """
                                alert_string_plain = alert_string_plain + \
                                    f"""\nExiste uma tendência de {tendency} nos dados - {accel_name_helper}"""
                                print('rule3 Fired')
                                rules_fired_array[1] = 3
                                #write_database(client, 3, last_ttsamp)
                                rules_Fired = rules_Fired + 1

                        # ====================================================================================================
                        # RULE 4
                        if rule == 'rule4':
                            # If the point is below the mean + 2 standard deviation
                            if (value < (mean-(2*stddev)) and previous_was_bigger):
                                count_rule4 = count_rule4+1
                                previous_was_lower = True
                                previous_was_bigger = False
                            # If the value is bigger and the last value was below mean+2*stdev,
                            elif (value > (mean+(2*stddev)) and previous_was_lower):
                                # then it also fits in the rule
                                count_rule4 = count_rule4+1
                                previous_was_bigger = True
                                previous_was_lower = False
                            else:  # Else, reset the counter
                                count_rule4 = 0
                            # Finally, check if the rule is fired or not
                            if count_rule4 >= QUERY_AMOUNT:
                                alert_string_HTML = alert_string_HTML + f"""\
                                <p>Existe muita oscilação (Além de um ruído comum) - {accel_name_helper}.</p>
                                """
                                alert_string_plain = alert_string_plain + \
                                    f"""\nExiste muita oscilação (Além de um ruído comum) - {accel_name_helper}."""
                                print('rule4 Fired')
                                rules_fired_array[2] = 4
                                #write_database(client, 4, last_ttsamp)
                                rules_Fired = rules_Fired + 1

                        # ====================================================================================================
                        # RULE 6
                        if rule == 'rule6':
                            if value > (mean+(1*stddev)) and previous_was_bigger:
                                count_rule6 = count_rule6 + 1
                                previous_was_lower = False
                            elif value < (mean-(1*stddev)) and previous_was_lower:
                                previous_was_bigger = False
                                count_rule6 += 1
                            elif value > mean+1*stddev:
                                previous_was_bigger = True
                                count_rule6 = 0
                            else:
                                previous_was_lower = True
                                count_rule6 = 0
                                if count_rule6 == 4:
                                    count_rule6 = -QUERY_AMOUNT
                                    alert_string_HTML = alert_string_HTML + f"""\
                                    <p>Existe uma FORTE tendência das amostras estarem ligeiramente fora de controle - {accel_name_helper}.</p>
                                    """
                                    alert_string_plain = alert_string_plain + \
                                        f"""\nExiste uma FORTE tendência das amostras estarem ligeiramente fora de controle - {accel_name_helper}."""
                                    print('rule6 Fired')
                                    rules_fired_array[3] = 6
                                    #write_database(client, 6, last_ttsamp)
                                    rules_Fired = rules_Fired + 1

        # End of each column loop and rules loop
        write_database(client, rules_fired_array, last_ttsamp)
        start_analysis = dt.strptime(
            tstamp[QUERY_AMOUNT-1], '%Y-%m-%dT%H:%M:%S.%fZ')
        end_analysis = dt.strptime(tstamp[0], '%Y-%m-%dT%H:%M:%S.%fZ')
        start_analysis_url = str(
            int(start_analysis.timestamp())-GRAFANA_URL_SHIFT_LESS)+'000'
        end_analysis_url = str(
            int(end_analysis.timestamp())+GRAFANA_URL_SHIFT)+'000'
        alert_string_HTML = alert_string_HTML + f"""
                    <br>Convém analisar a <a href = "http://193.136.195.105:3000/d/dEX-6D_nk/zani-catraport-accel?orgId=1&from={start_analysis_url}&to={end_analysis_url}&refresh=10s">Dashboard</a><br>
                    <p>O tempo analisado foi: {start_analysis} até {end_analysis}</p>
            </body>
        </html>
        """
        alert_string_plain = alert_string_plain + f"""Convém analisar a Dashboard*\n\n*URL: http://193.136.195.105:3000/d/dEX-6D_nk/zani-catraport-accel?orgId=1&from={start_analysis_url}&to={end_analysis_url}&refresh=10s\n
            O tempo analisado foi: {start_analysis} até {end_analysis}
            """
        # If any of the rules fired, for each column
        if rules_Fired != 0:
            send_email(alert_string_HTML, alert_string_plain, rules_Fired)
        else:
            print('No Rules fired')
        # Sleep for X seconds, to check again.
        # X = IOTAWATT_SAMPLE_TIME (sample time of IoTaWatt, in seconds)*QUERY_AMOUNT/2 (Half the amount of data analized, to analize with previous data)
        # It will sleep for 0.2*7 = 1.4 secs in the current config
        time.sleep(IOTAWATT_SAMPLE_TIME*floor(QUERY_AMOUNT/2))


def send_email(stringHTML: str, stringPlain: str, rulesFired: int):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "remote.rasp.catra@gmail.com"  # Enter your address
    receiver_email = "remote.ra.sp.catra@gmail.com"  # Enter receiver address
    password = 'catraport2020'
    message = MIMEMultipart("alternative")
    alert_txt = 'alertas' if rulesFired > 1 else 'alerta'  # To be prettier...
    message["Subject"] = f"Alertas na Catraport - Acelerômetro ({rulesFired} {alert_txt})"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(stringPlain, "plain")
    part2 = MIMEText(stringHTML, "html")
    message.attach(part1)
    message.attach(part2)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


def write_database(client: InfluxDBClient, values, time_stamp):
    client.switch_database('alerts')
    for value, index in zip(values, [1, 3, 4, 6]):
        json_body = [{"measurement": f'Alert_Accel_{index}', "time": time_stamp, "fields": {
            "value": value}}]
        client.write_points(json_body, time_precision='s')
    client.switch_database('iotawatt')


if __name__ == "__main__":
    main()
