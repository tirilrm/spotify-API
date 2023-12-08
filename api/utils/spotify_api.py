import requests


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def get_spotify_id(token):
    url = 'https://api.spotify.com/v1/me'
    headers = get_auth_header(token)

    response = requests.get(url, headers=headers).json()['id']
    return response


def get_top_artists_and_genres(token):
    url = 'https://api.spotify.com/v1/me/top/artists'
    headers = get_auth_header(token)

    response = requests.get(url, headers=headers).json()['items']

    top_artists = [artist['name'] for artist in response]
    
    top_genres = []
    genre_list = [genre['genres'] for genre in response]
    for genre_l in genre_list:
        for genre in genre_l:
            top_genres.append(genre)
    top_genres = list(set(top_genres)) # remove duplicates


    return top_artists, top_genres
