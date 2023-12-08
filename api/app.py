import urllib.parse
import requests
from flask import Flask, request, redirect, jsonify, session, render_template
#from api.utils.credentials import CLIENT_SECRET, CLIENT_ID
from api.utils.spotify_api import get_top_artists_and_genres, get_spotify_id
from api.utils.ticketmaster_api import get_events_based_on_genre

import os
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CLIENT_ID = os.getenv('CLIENT_ID')

random_key = os.urandom(12)

REDIRECT_URI = 'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

app = Flask(__name__)
app.secret_key = random_key


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/login")
def login():
    scope = 'user-read-private user-read-email user-top-read'

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    return redirect(auth_url)


@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})

    if 'code' in request.args:
        # get access token
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()

        session['access_token'] = token_info['access_token']

        return redirect('/homepage')


@app.route('/homepage')
def homepage():
    if 'access_token' not in session:
        return redirect('/login')

    # Request spotify top arists
    get_spotify_id(session['access_token'])
    top_artists, top_genres = get_top_artists_and_genres(session['access_token'])
    city = 'london'

    # Get events based on genres
    events = get_events_based_on_genre(top_genres, city)

    # return jsonify(results)
    return render_template('events_temp.html',
                           top_artists=top_artists,
                           top_genres=top_genres,
                           events=events)


# if __name__ == '__main__':
#     app.run(debug=True)
