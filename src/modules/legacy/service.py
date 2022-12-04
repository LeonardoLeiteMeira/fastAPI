import modules.legacy.repository as repository

async def get_processed_files():
    json_list = await repository.get_list_of_legacy_files_processed()
    files_list:list = [file["file"] for file in json_list]
    return files_list

async def get_file_by_name(file_name:str):
    result =  await repository.get_file_by_name(file_name)
    return result

async def get_all_files():
    result =  await repository.get_all_files()
    return result
