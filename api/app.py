import urllib.parse
import requests
from flask import Flask, request, redirect, jsonify, session
from utils.credentials import CLIENT_SECRET, CLIENT_ID
from api.utils.spotify_api import get_artists, get_spotify_id
import os

random_key = os.urandom(12)

REDIRECT_URI = 'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

app = Flask(__name__)
app.secret_key = random_key


@app.route("/")
def index():
    return "Welcome to my Spotify App <a href='/login'> Logic with Spotify</a>"


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

    get_spotify_id(session['access_token'])
    results = get_artists(session['access_token'])
    return jsonify(results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
