import requests
import json


def get_auth_header(token):
    return {"Authorization" : "Bearer " + token}


def get_spotify_id(token):
    url = 'https://api.spotify.com/v1/me'
    headers = get_auth_header(token)

    response = requests.get(url, headers=headers).json()['id']
    return response


def get_artists(token):
    url = 'https://api.spotify.com/v1/me/top/artists'
    headers = get_auth_header(token)

    response = requests.get(url, headers=headers).json()['items']

    artists = []
    for i in range(len(response)):
        artists.append({key: response[i][key] for key in ['name', 'genres']})

    return artists