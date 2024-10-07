from classes import Track, User, Listen_history
from extract import request, get_data, extract
from transform import parse_tracks, parse_users, parse_listen_history, transform, formatDT
from load import load

from datetime import datetime
from time import time, sleep
import subprocess
from os import environ

environ["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"

from src.moovitamix_fastapi.classes_out import gender_list, genre_list

try:
    request('tracks') # ping the API to see if it is live
except:
    subprocess.Popen(["python", "-m", "uvicorn", "main:app", "--reload"], cwd="src/moovitamix_fastapi") 
    timeout = time() + 60*5 # 5 minutes from now
    while True:
        if time() > timeout:
            raise Exception('API connexion timeout')
        try:
            request('tracks')
        except:
            sleep(1)
        else:
            break

full_test_data = []

def test_request_tracks():
    data = request('tracks')
    assert isinstance(data, dict)
    assert isinstance(data['page'], int)
    items = data['items']
    assert isinstance(items, list)
    item = items[0]
    assert isinstance(item, dict)
    assert isinstance(item['id'], int)
    assert isinstance(item['duration'], str)
    assert isinstance(item['created_at'], str) # required type conversion
    assert isinstance(datetime.strptime(item['created_at'], formatDT), datetime)

def test_request_users():
    data = request('users')
    size = data['size']
    assert isinstance(data, dict)
    assert isinstance(data['total'], int)
    items = data['items']
    assert isinstance(items[0], dict)
    assert len(items) == size

def test_request_listen_history():
    data = request('listen_history')
    assert isinstance(data, dict)
    items = data['items']
    assert isinstance(items, list)
    item = items[data['size']-1]
    assert isinstance(item, dict)
    assert isinstance(item['user_id'], int)

def test_get_data():
    data = get_data('tracks')
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
    assert isinstance(data[0]['artist'], str)

def test_extract():
    full_test_data = extract()
    assert isinstance(full_test_data, list)
    tracks_data = full_test_data[0]
    assert isinstance(tracks_data, list)
    track_data = tracks_data[0]
    assert isinstance(track_data, dict)
    assert isinstance(track_data['album'], str)

def test_parse_tracks():
    tracks_data = get_data('tracks')
    tracks_parse_data = parse_tracks(tracks_data)
    assert isinstance(tracks_parse_data, list)
    track_parse_data = tracks_parse_data[0]
    assert isinstance(track_parse_data, Track)
    assert isinstance(track_parse_data.id, int)
    assert isinstance(track_parse_data.artist, str)
    assert isinstance(track_parse_data.genres, str) # Track.genres NOT IN genre_list()
    assert isinstance(track_parse_data.duration, str) # duration is formated as a string
    assert isinstance(track_parse_data.created_at, datetime)

def test_parse_users():
    users_data = get_data('users')
    users_parse_data = parse_users(users_data)
    assert isinstance(users_parse_data, list)
    assert isinstance(users_parse_data[0], User)
    assert users_parse_data[0].gender in gender_list()
    assert users_parse_data[0].favorite_genres in genre_list()

def test_parse_listen_history():
    listen_history_data = get_data('listen_history')
    listen_history_parse_data = parse_listen_history(listen_history_data)
    assert isinstance(listen_history_parse_data, list)
    assert isinstance(listen_history_parse_data[0], Listen_history)
    assert isinstance(listen_history_parse_data[0].created_at, datetime)

def test_transform():
    full_test_data = transform(extract())
    assert isinstance(full_test_data, list)
    assert len(full_test_data) == 3
    tracks_data = full_test_data[0]
    assert isinstance(tracks_data, list)
    track_data = tracks_data[0]
    assert isinstance(track_data, Track)

def test_load():
    session = load(transform(extract()))

    print('\nPrinting the first 10 tracks from the database:')
    print('----------------------------------------\n')
    results = session.query(Track).all()
    for r in range(0, 10):
        print(results[r])
    print(f'\nNumber of tracks in the database: {len(results)}')

    print('\nPrinting the first 10 users from the database:')
    print('----------------------------------------\n')
    results = session.query(User).all()
    for r in range(0, 10):
        print(results[r])
    print(f'\nNumber of users in the database: {len(results)}')

    print('\nPrinting the first 10 listen historys from the database:')
    print('----------------------------------------\n')
    results = session.query(Listen_history).all()
    for r in range(0, 10):
        print(results[r])
    print(f'\nNumber of listen historys in the database: {len(results)}')

if __name__ == '__main__':

    test_request_tracks()
    test_request_users()
    test_request_listen_history()
    test_get_data()
    test_extract()
    test_parse_tracks()
    test_parse_users()
    test_parse_listen_history()
    test_transform()
    test_load()
    
    print('\nAll data pipeline components operational\n')