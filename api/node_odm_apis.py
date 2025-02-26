import json
import sys
import time
import os
from api_utils import request_url, get_request, post_request
from utils import get_image_list

USERNAME = "hasitha"
PASSWORD = "hasdha.1"
IMAGE_DIR ='../data/DJI_202311211138_007_Create-Area-Route12'
MAX_TASK_WAITING_SECONDS = 100

# Authentication
def get_token(username, password):
    url = request_url("token-auth/")
    api_response = post_request(url,
                                data={'username': username, 'password': password})
    if 'token' in api_response:
        return api_response['token']
    else:
        print(f"get_token|token not found in api_response: {api_response}")
        return None

# Projects
def get_projects():
    url = request_url("projects/")
    token = get_token(USERNAME, PASSWORD)
    print(f"get_projects|url : {url}")
    api_response = get_request(url, token=token)
    print(f"get_projects|api_response : {api_response.json()}")
    return api_response.json()

def create_project(project_name):
    url = request_url("projects/")
    token = get_token(USERNAME, PASSWORD)
    print(f"create_project|url : {url}")
    api_response = post_request(url,
                                token=token,
                                data={'name': project_name})
    print(f"create_project|api_response : {api_response}")
    return api_response['id']

def get_project(project_id):
    url = request_url(f"projects/{project_id}/")
    token = get_token(USERNAME, PASSWORD)
    print(f"get_projects|url : {url}")
    api_response = get_request(url, token=token)
    print(f"get_projects|api_response : {api_response.json()}")
    return api_response.json()

def create_project_task(dir_path, project_id, options):
    images = get_image_list(dir_path)
    print(f"create_project_task|images : {images}")
    options = json.dumps(options)
    token = get_token(USERNAME, PASSWORD)
    url = request_url(f"projects/{project_id}/tasks/")
    print(f"create_project_task|url : {url}")
    api_response = post_request(url,
                                token=token,
                                data={'options' : options},
                                files=images)
    print(f"create_project_task|api_response : {api_response}")
    return project_id, api_response['id']

def get_project_task(project_id, task_id):
    url = request_url(f"projects/{project_id}/tasks/{task_id}/")
    print(f"get_project_task|url : {url}")
    token = get_token(USERNAME, PASSWORD)
    api_response = get_request(url,token=token)
    print(f"get_project_task|api_response : {api_response.json()}")
    return api_response.json()

def download_asset(download_dir, project_id, task_id, asset):
    os.makedirs(download_dir, exist_ok=True)
    token = get_token(USERNAME, PASSWORD)
    task_info = get_project_task(project_id, task_id)
    if task_info['running_progress'] == 1.0:
        print("Task has completed!")
        url = request_url(f"projects/{project_id}/tasks/{task_id}/download/{asset}")
        print(f"download_asset|url : {url}")
        api_response = get_request(url, token=token, stream=True)
        print(f"download_asset|api_response : {api_response}")
        asset_path = f"{download_dir}/{asset}"
        with open(asset_path, 'wb') as f:
            print("download_asset|Downloading, in progress...")
            for chunk in api_response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"download_asset|asset {asset} is downloaded to {download_dir}")
    elif task_info['last_error'] is not None:
        print("download_asset|Task failed: {}".format(task_info))
        sys.exit(1)
    else:
        print(f"download_asset|Current running progress is {task_info['running_progress']*100}%")
        sleep_time = int(MAX_TASK_WAITING_SECONDS * (1 - task_info['running_progress']))
        time.sleep(sleep_time)
        download_asset(download_dir, project_id, task_id, asset)

# if __name__ == "__main__":
#     projects = get_projects()
#     for project in projects:
#         project_id = project['id']
#         tasks = project['tasks']
#         if tasks:
#             task_id = tasks[0]
#             get_project_task(project_id, task_id)

# if __name__ == "__main__":
#     project_id = create_project("testing3")
#     # project_id, task_id = create_project_task(IMAGE_DIR, project_id, [{'name': "orthophoto-resolution", 'value': 24}])
#     # auto-boundary:true, dsm:true, dem-resolution:2, pc-quality:high
#     project_id, task_id = create_project_task(IMAGE_DIR, project_id, [
#         {'name': 'auto-boundary', 'value': True},
#         {'name': 'dsm', 'value': True},
#         {'name': 'dem-resolution', 'value': '2'},
#         {'name': 'pc-quality', 'value': 'high'}
#     ])
#     dir_path = f"../download/project_id_{project_id}"
#     download_asset(dir_path, project_id, task_id, 'dsm.tif')

if __name__ == "__main__":
    project_id = create_project("testing4")
    # project_id, task_id = create_project_task(IMAGE_DIR, project_id, [{'name': "orthophoto-resolution", 'value': 24}])
    # auto-boundary:true, dsm:true, dem-resolution:2, pc-quality:high
    project_id, task_id = create_project_task(IMAGE_DIR, project_id, [
        {'name': 'auto-boundary', 'value': True},
        {'name': 'dtm', 'value': True},
        {'name': 'dsm', 'value': True},
        {'name': 'smrf', 'value': True},
        {'name': 'pc-quality', 'value': 'high'}
    ])
    dir_path = f"../download/project_id_{project_id}"
    download_asset(dir_path, project_id, task_id, 'dtm.tif')

# if __name__ == "__main__":
#     project_id = 15
#     project_info = get_project(project_id)
#     task_id = project_info['tasks'][0]
#     get_project_task(project_id, task_id)
#     dir_path = f"../download/project_id_{project_id}"
#     download_asset(dir_path, project_id, task_id, 'orthophoto.tif')