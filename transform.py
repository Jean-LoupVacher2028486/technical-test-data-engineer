from classes import Track, User, Listen_history
from datetime import datetime

# format for the datetime.strptime type conversion from String to DateTime
formatDT = '%Y-%m-%dT%H:%M:%S.%f'

def parse_tracks(items):
    tracks = []

    for item in items:
        track = Track(item['id'],
                      item['name'],
                      item['artist'],
                      item['songwriters'],
                      item['duration'],
                      item['genres'],
                      item['album'],
                      datetime.strptime(item['created_at'], formatDT),
                      datetime.strptime(item['updated_at'], formatDT))

        tracks.append(track)
    return tracks

def parse_users(items):
    users = []

    for item in items:
        user = User(item['id'],
                    item['first_name'],
                    item['last_name'],
                    item['email'],
                    item['gender'],
                    item['favorite_genres'],
                    datetime.strptime(item['created_at'], formatDT),
                    datetime.strptime(item['updated_at'], formatDT))
        
        users.append(user)
    return users

def parse_listen_history(items):
    listen_historys = []

    for item in items:
        for track in item['items']:
            listen_history = Listen_history(item['user_id'],
                                            track,
                                            datetime.strptime(item['created_at'], formatDT),
                                            datetime.strptime(item['updated_at'], formatDT))
            
            listen_historys.append(listen_history)
    return listen_historys

def transform(json):
    data = []

    data.append(parse_tracks(json[0]))
    data.append(parse_users(json[1]))
    data.append(parse_listen_history(json[2]))

    return data