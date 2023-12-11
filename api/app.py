# app.py

import urllib.parse
import requests
from flask import Flask, request, redirect, jsonify, session, render_template
from api.utils.spotify_api import get_top_artists_and_genres, get_spotify_id
from api.utils.ticketmaster_api import get_events
from api.utils.db_query import execute_query
import os

CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CLIENT_ID = os.getenv('CLIENT_ID')

random_key = os.urandom(12)

REDIRECT_URI = os.environ.get('REDIRECT_URI', 'http://localhost:5000/callback')

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

app = Flask(__name__)
app.secret_key = random_key


def get_liked_events():

    spotify_id = get_spotify_id(session['access_token'])
    query = f'''
    SELECT event_id from liked_events WHERE spotify_id = '{spotify_id}'
    '''
    liked_events = execute_query(query)

    return [e[0] for e in liked_events]


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

# Mock data for testing
mock_data = {
    'events': [
        {
            'name': 'Event 1',
            'event_date': '2023-12-31',
            'event_time': '20:00:00',
            'city': 'City 1',
            'country': 'Country 1',
            'venue_name': 'Venue 1',
            'price_range': '$$$',
            'image_url': 'https://example.com/event1.jpg',
            'url': 'https://example.com/event1',
            'id': 'event1_id'
        },
        {
            'name': 'Event 2',
            'event_date': '2023-12-31',
            'event_time': '20:00:00',
            'city': 'City 1',
            'country': 'Country 1',
            'venue_name': 'Venue 1',
            'price_range': '$$$',
            'image_url': 'https://example.com/event2.jpg',
            'url': 'https://example.com/event2',
            'id': 'event2_id'
        },
    ],
    'liked_events': ['event1_id']  # IDs of liked events
}


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
        # For testing, you can set the access token directly in the session
        session['access_token'] = 'your_mock_access_token'


        return redirect('/homepage')


# Endpoint for testing with mock data
@app.route('/test')
def test():
    # Return mock data instead of making actual requests
    '''
    return render_template('homepage.html', top_artists=mock_data['top_artists'], top_genres=mock_data['top_genres'])
    '''
    # Return mock data instead of making actual requests
    return render_template('events_results.html', events=mock_data['events'], liked_events=mock_data['liked_events'])

# Add this route for testing the liked_events page
@app.route('/test_liked_events')
def test_liked_events():
    # Mock data for testing
    mock_liked_events = ['event_id_1', 'event_id_2']  # Replace with actual event IDs

    # Render the liked_events page with mock data
    liked_events_info = get_events(event_id_list=mock_liked_events)  # Replace with actual function call
    return render_template('liked_events.html', liked_events_info=liked_events_info)



@app.route('/homepage')
def homepage():
    if 'access_token' not in session:
        return redirect('/login')

    # Request spotify top arists
    top_artists, top_genres = get_top_artists_and_genres(session['access_token'])

    # return jsonify(results)
    return render_template('homepage.html',
                           top_artists=top_artists,
                           top_genres=top_genres)


@app.route('/liked_events')
def liked_events():
    if 'access_token' not in session:
        return redirect('/login')

    liked_events = get_liked_events()
    if liked_events:
        liked_events_info = get_events(event_id_list=liked_events)  # get event info by event id
    else:
        liked_events_info = []
    return render_template('liked_events.html', liked_events_info=liked_events_info)


@app.route('/events_results', methods=["POST"])
def event_search():
    if 'access_token' not in session:
        return redirect('/login')
    city = request.form.get('city')
    top_genres = get_top_artists_and_genres(session['access_token'])[1]

    # Get events based on genres
    liked_events = get_liked_events()
    events = get_events(genres=top_genres, city=city)

    return render_template('events_results.html',
                           events=events,
                           liked_events=liked_events)


@app.route('/like', methods=["POST"])
def like():
    if 'access_token' not in session:
        return redirect('/login')
    spotify_id = get_spotify_id(session['access_token'])
    event_id = request.form.get('eventID')
    query = f'''
    INSERT INTO liked_events (spotify_id, event_id)
    VALUES ('{spotify_id}', '{event_id}')
    ON CONFLICT DO NOTHING
    '''
    execute_query(query, "insert")
    return 'Ok'


@app.route('/unlike', methods=["POST"])
def unlike():
    if 'access_token' not in session:
        return redirect('/login')
    spotify_id = get_spotify_id(session['access_token'])
    event_id = request.form.get('eventID')
    query = f'''
    DELETE FROM liked_events
    WHERE spotify_id='{spotify_id}'
        AND event_id='{event_id}'
    '''
    execute_query(query, "delete")
    return 'Ok'


if __name__ == '__main__':
    app.run(debug=True)


# unit test
def process_query(query):
    if "test" in query:
        return "Test has passed"

    @app.route("/query")
    def query():
        return process_query(request.args.get('q', default="", type=str))
