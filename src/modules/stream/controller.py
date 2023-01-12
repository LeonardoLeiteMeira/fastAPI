from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from influxdb_client import InfluxDBClient, Point, BucketRetentionRules

router = APIRouter(tags=["Stream"])

url = 'http://localhost:8086'
token = '2Wc71suOxmK_X1iQ8pjJd2RAwrn_6azqdQ9vbcW6cUJ3zQv33SPDHjoiqbrmV0VxSACCS9t2_rGql9CxAbca_g=='
org = 'leonardo'
bucket = 'python_test'
client = InfluxDBClient(url=url, token=token, org=org)

async def fake_video_streamer():
    for i in range(10000000):
        # yield b"test"
        yield "{} some fake video bytes\n".format(i)

async def influx_data():
    query = 'from(bucket: "python_test")\
    |> range(start: -12h)'
    data = client.query_api().query_stream(org=org, query=query)
    async for record in data:
            yield record

@router.get("/")
async def simple_get():
    return StreamingResponse(fake_video_streamer())


@router.get("/influx")
async def get_influx_data():
    return StreamingResponse(influx_data())