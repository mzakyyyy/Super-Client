import requests

def get_bearer_token():
    url = 'https://property-kpr.azurewebsites.net/login'
    data = {"username": "zaky@mail.com", "password": "password"}
    response = requests.post(url, data=data)
    jsonresponse = response.json()
    bearertoken = str(jsonresponse['access_token'])
    return bearertoken


def format_get(url: str):
    link = url
    headers = {"Authorization": f'Bearer {get_bearer_token()}'}
    response = requests.get(link, headers=headers)
    jsonresponse = response.json()
    return jsonresponse