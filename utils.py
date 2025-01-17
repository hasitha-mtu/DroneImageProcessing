import requests

AUTH_TOKEN_URL = 'http://localhost:8000/api/token-auth/'

def get_token(username, password):
    res = requests.post(AUTH_TOKEN_URL,
                    data={'username': username,
                          'password': password}).json()
    if 'token' in res:
        return res['token']
    else:
        print(f"get_token|token not found in res: {res}")
        return None

if __name__ == "__main__":
    # token = get_token("hasitha", "Hasitha@4805")
    token = get_token("hasitha", "hasdha.1")
    print(f"generated token : {token}")