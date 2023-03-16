import requests

headers = {'X-Token': 'f313@edf34&4*33#324gj56'}


def read(mortality_rate_id):
    url = 'https://library.treasurance.info/out-api/v2/mortality-rate/get-value?id=%s' % mortality_rate_id
    response = requests.post(url, headers=headers)
    return response.json()


def create(data):
    url = 'https://library.treasurance.info/out-api/v2/mortality-rate/create'
    response = requests.post(url, headers=headers, json=data)
    return response.json()


def delete(mortality_rate_id):
    url = 'https://library.treasurance.info/out-api/v2/mortality-rate/delete?id=%s' % mortality_rate_id
    response = requests.post(url, headers=headers)
    return response.json()
