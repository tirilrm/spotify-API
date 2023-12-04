import requests


BASE_URL = 'https://app.ticketmaster.com/discovery/v2/events?apikey=r6gVnBhupGQ6x6tIDaVQpfoNtpwe67EQ'
query = '&locale=*&countryCode=FR&classificationName=rock,pop'

response = requests.get(BASE_URL + query).json()
print(response)