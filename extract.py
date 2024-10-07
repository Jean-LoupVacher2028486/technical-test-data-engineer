import requests

# base URL to request data from the API
url = 'http://127.0.0.1:8000/'

# request the API data at specified endpoint (str) and page (int)
def request(endpoint, page=1):
    return requests.get(url + endpoint + f'?page={page}').json()

# get data from all pages at given endpoint of the API
def get_data(endpoint):
    data = []
    n_pages = request(endpoint)['pages']

    for page in range(1, n_pages+1):
        items = request(endpoint, page)['items']

        for item in items:
            data.append(item)

    return data

# get all the data for tracks, users and listen_history
def extract():
    data = []

    data.append(get_data('tracks'))
    data.append(get_data('users'))
    data.append(get_data('listen_history'))

    return data