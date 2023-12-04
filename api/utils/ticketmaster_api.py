import requests
from credentials import TICKETMASTER_APIKEY

BASE_URL = 'https://app.ticketmaster.com/discovery/v2/events?apikey='
query = '&locale=*&countryCode=FR&classificationName=rock,pop'

response = requests.get(BASE_URL + TICKETMASTER_APIKEY + query).json()
print(response)
