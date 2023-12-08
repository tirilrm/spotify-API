from flask import Flask, render_template, request, redirect, session, jsonify
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    # add spotify API details 

    # Redirect to the spotify log in page
    return redirect(auth_url)

    # Redirect user to the events page
    return redirect('/events')


@app.route('/callback')
def callback():
    # add code from spotify_api branch


@app.route('/homepage')
def homepage():
    if 'access_token' not in session:
        return redirect('/login')
    # retrieve spotify user information
    # (add code from spotify_api branch)

    #add ticketmaster API for event information

return render_template('events.html', top_artists=top_artists, events_data=events_data)


if __name__ == '__main__':
    app.run(debug=True)