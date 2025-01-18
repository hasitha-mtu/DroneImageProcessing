import requests
import glob
import json
import sys
from requests import codes as status_codes
import time

AUTH_TOKEN_URL = 'http://localhost:8000/api/token-auth/'
CREATE_PROJECT_URL = 'http://localhost:8000/api/projects/'
IMAGE_DIR ='data/DJI_202311211138_007_Create-Area-Route12'

def get_token(username, password):
    res = requests.post(AUTH_TOKEN_URL,
                    data={'username': username,
                          'password': password}).json()
    if 'token' in res:
        return res['token']
    else:
        print(f"get_token|token not found in res: {res}")
        return None


def create_project(token, project_name):
    res = requests.post(CREATE_PROJECT_URL,
                        headers={'Authorization': 'JWT {}'.format(token)},
                        data={'name': project_name}).json()
    if 'id' in res:
        return res['id']
    else:
        print(f"create_project|id not found in res: {res}")
        return None

def get_image_list(dir_path):
    image_paths = glob.glob(f"{dir_path}/*.JPG")
    print(f'get_image_list|image_paths : {image_paths}')
    image_files = []
    for image_path in image_paths:
        image = ('images', (image_path, open(image_path, 'rb'), 'image/jpg'))
        image_files.append(image)
    return image_files

def process_images(username, password, project_name, dir_path):
    images = get_image_list(dir_path)
    print(f"process_images|images : {images}")
    options = json.dumps([{'name': "orthophoto-resolution", 'value': 24}])
    token = get_token(username, password)
    print(f"process_images|token : {token}")
    project_id = create_project(token, project_name)
    print(f"process_images|project_id : {project_id}")
    process_image_res = requests.post('http://localhost:8000/api/projects/{}/tasks/'.format(project_id),
                        headers={'Authorization': 'JWT {}'.format(token)},
                        files=images,
                        data={
                            'options': options
                        }).json()
    print(f"process_images|process_image_res : {process_image_res}")
    task_id = process_image_res['id']
    print(f"process_images|task_id : {task_id}")
    while True:
        task_status_res = requests.get('http://localhost:8000/api/projects/{}/tasks/{}/'.format(project_id, task_id),
                           headers={'Authorization': 'JWT {}'.format(token)}).json()
        print(f"process_images|task_status_res : {task_status_res}")
        if task_status_res['pending_action'] is None:
            print("Task has completed!")
            complete_res = requests.get(
                "http://localhost:8000/api/projects/{}/tasks/{}/download/orthophoto.tif".format(project_id, task_id),
                headers={'Authorization': 'JWT {}'.format(token)},
                stream=True)
            print(f"process_images|complete_res : {complete_res}")
            with open("orthophoto.tif", 'wb') as f:
                for chunk in complete_res.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print("Saved ./orthophoto.tif")
            break
        elif task_status_res['last_error'] is not None:
            print("Task failed: {}".format(task_status_res))
            sys.exit(1)
        else:
            print("Processing, hold on...")
            time.sleep(3)
    pass

if __name__ == "__main__":
    # token = get_token("hasitha", "Hasitha@4805")
    # token = get_token("hasitha", "hasdha.1")
    # print(f"generated token : {token}")
    # images = get_image_list(IMAGE_DIR)
    # print(f"images : {images}")
    process_images("hasitha", "Hasitha@4805", "code_proj3", IMAGE_DIR)
