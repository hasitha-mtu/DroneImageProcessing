import requests
from urllib.parse import urljoin

BASE_URL = 'http://localhost:8000/api/'


def request_url(api_section):
    return urljoin(BASE_URL, api_section)

def get_request(url, token = None, headers = None, **kwargs):
    if token:
        if headers:
            headers['Authorization'] = 'JWT {}'.format(token)
        else:
            headers = {'Authorization': 'JWT {}'.format(token)}
    response = requests.get(url=url, headers= headers, **kwargs)
    if response.status_code == 200:
        return response
    else:
        print(f"get_request|url: {url}|headers: {headers}|kwargs: {kwargs}")
        print(f"get_request|response: {response}")
        print("Failed to retrieve data", response.status_code)
        return None

def post_request(url, token = None, headers = None, **kwargs):

    if token:
        if headers:
            headers['Authorization'] = 'JWT {}'.format(token)
        else:
            headers = {'Authorization': 'JWT {}'.format(token)}
    response = requests.post(url=url, headers= headers, **kwargs)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 201:
        return response.json()
    else:
        print(f"post_request|url: {url}|headers: {headers}|kwargs: {kwargs}")
        print(f"post_request|response: {response}")
        print("Failed to retrieve data", response.status_code)
        return None
