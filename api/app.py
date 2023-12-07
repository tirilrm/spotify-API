from flask import Flask, render_template, request, redirect, session, jsonify
from datetime import datetime
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route(/"login", methods=["POST"])
def login():
    # Retrieve the Spotify username and location from the form submission
    username = request.form.get('username')
    location = request.form.get('location')

    # Here, you can use the username and location as needed
    # For example, you can store them in the session
    session['spotify_username'] = username
    session['user_location'] = location

    # Redirect user to the events page
    return redirect('/events')

@app.route('/events')
def events():
    # Fetch music events based on Spotify username and location
    # You can use the session data (username and location) to customize the events
    # For example, fetch top artists based on the Spotify username and search for events in the specified location
    return render_template('events.html')