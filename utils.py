import requests

def get_token(username, password):
    res = requests.post('http://localhost:8000/api/token-auth/',
                    data={'username': username,
                          'password': password}).json()
    print(f"get_token|res: {res}")
    token = res['token']
    return token

if __name__ == "__main__":
    token = get_token("hasitha", "Hasitha@4805")
    print(f"generated token : {token}")