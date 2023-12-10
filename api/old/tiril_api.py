# from flask import Flask, render_template, request
# import re
import requests


# @app.route("/get-your-recommended-concerts", methods=["POST"])
def get_concerts():

	url = "https://www.eventbriteapi.com/v3/events/search/"

	api_key = "BSPT5EO4GDBMG2ME4RD5"
	city = "London"

	headers = {
		"Authorization": f"Bearer {api_key}",
	}
	params = {
		"location.address": city,
	}

	response = requests.get(url, headers=headers, params=params)

	if response.status_code == 200:
		return response.json()  # Returns the JSON response with concert details
	else:
		return f"Error: {response.status_code}"


# Usage example
concerts = get_concerts()
print(concerts)
