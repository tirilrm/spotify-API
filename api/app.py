from flask import Flask, render_template, request, redirect, session, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    # Retrieve the Spotify username and location from the form submission
    username = request.form.get('username')
    location = request.form.get('location')

    # Storing username and location in the session
    session['spotify_username'] = username
    session['user_location'] = location

    # Redirect user to the events page
    return redirect('/events')

@app.route('/events')
def events():
    return render_template('events.html')

if __name__ == '__main__':
    app.run(debug=True)