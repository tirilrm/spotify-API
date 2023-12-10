# from flask import Flask, render_template, request
# from api.utils.credentials import TICKETMASTER_APIKEY
import requests
import os
TICKETMASTER_APIKEY = os.getenv('TICKETMASTER_APIKEY')

# import csv


# app = Flask(__name__)


BASE_URL = f'https://app.ticketmaster.com/discovery/v2/events?apikey={TICKETMASTER_APIKEY}&locale=*'


# @app.route('/')
# def index():
#     return render_template('index.html')


# @app.route('/search/events', methods=['POST'])
# def search_events_route():
#     keyword = request.form['event_keyword']
#     event_results, event_data = search_events(keyword)
#     return render_template('results.html', events=event_results, data=event_data)


# @app.route('/search/attractions', methods=['POST'])
# def search_attractions_route():
#     keyword = request.form['attraction_keyword']
#     attraction_results = search_attractions(keyword)
#     return render_template('attractions_results.html', attractions=attraction_results)


# @app.route('/search/classifications', methods=['POST'])
# def search_classifications_route():
#     keyword = request.form['classification_keyword']
#     classification_results = search_classifications(keyword)
#     return render_template('classifications_results.html', classifications=classification_results)


# @app.route('/search/venues', methods=['POST'])
# def search_venues_route():
#     keyword = request.form['venue_keyword']
#     venue_results = search_venues(keyword)
#     return render_template('results.html', venues=venue_results)


# def search_events(keyword):
#     query = f'events?apikey={TICKETMASTER_APIKEY}&keyword={keyword}'
#     response = requests.get(BASE_URL + query).json()
#     # print(response)
#     if '_embedded' in response and 'events' in response['_embedded']:
#         events = response['_embedded']['events']

#         # Extract and write to CSV
#         data = []
#         with open('events.csv', 'w', newline='') as file:
#             writer = csv.writer(file)

#             # Write CSV header
#             writer.writerow(['Name', 'ID', 'Locale', 'Genres', 'SubGenres', 'Segments', 'Venue', 'Attraction',
#                              'VenueType', 'PostalCode', 'Address', 'ImageURL', 'ImageWidth', 'ImageHeight'])

#             for event in events:
#                 name = event.get('name', '')
#                 event_id = event.get('id', '')
#                 locale = event.get('locale', '')

#                 # Extract genre, sub_genre, and segment from all classifications
#                 genres = []
#                 sub_genres = []
#                 segments = []

#                 # print(event.keys())

#                 if 'classifications' in event.keys():
#                     for classification in event['classifications']:
#                         # Extracting information from the primary segment
#                         segment_name = classification.get('segment', {}).get('name', '')
#                         segments.append(segment_name)

#                         # Extracting information from the primary genre
#                         genre_name = classification.get('genre', {}).get('name', '')
#                         genres.append(genre_name)

#                         # Extracting information from the tertiary sub-genre
#                         sub_genre_name = classification.get('subGenre', {}).get('name', '')
#                         sub_genres.append(sub_genre_name)

#                 # Use a delimiter (e.g., comma) to join multiple values into a single string
#                 segment = ', '.join(segments)
#                 genre = ', '.join(genres)
#                 sub_genre = ', '.join(sub_genres)
#                 venue_name = ''
#                 if '_embedded' in event and 'venues' in event['_embedded'] and event['_embedded']['venues']:
#                     venue_name = event['_embedded']['venues'][0]['name'] if 'name' in event['_embedded']['venues'][0] else ''

#                 attraction_name = ''
#                 if '_embedded' in event and 'attractions' in event['_embedded'] and event['_embedded']['attractions']:
#                     attraction_name = event['_embedded']['attractions'][0]['name'] if 'name' in event['_embedded']['attractions'][0] else ''

#                 # Extract venue information
#                 venue_info = event['_embedded']['venues'][0] if '_embedded' in event and 'venues' in event['_embedded'] and event['_embedded']['venues'] else {}
#                 venue_type = venue_info.get('type', '')
#                 postal_code = venue_info.get('postalCode', '')
#                 address = venue_info.get('address', '')

#                 # Extract image information
#                 image_info = event.get('images', [{}])[0]
#                 image_url = image_info.get('url', '')
#                 image_width = image_info.get('width', '')
#                 image_height = image_info.get('height', '')

#                 # Write to CSV
#                 writer.writerow([name, event_id, locale, genre, sub_genre, segment, venue_name, attraction_name,
#                                  venue_type, postal_code, address, image_url, image_width, image_height])

#                 data.append({
#                     'EventName': name,
#                     'EventID': event_id,
#                     'Genre': genre,
#                     'SubGenre': sub_genre,
#                     'Segment': segment,
#                     'Venue': venue_name,
#                     'Attraction': attraction_name,
#                     'VenueType': venue_type,
#                     'PostalCode': postal_code,
#                     'Address': address,
#                     'ImageURL': image_url,
#                     'ImageWidth': image_width,
#                     'ImageHeight': image_height
#                 })

#         return events, data
#     else:
#         return None


# def search_attractions(keyword):
#     query = f'attractions?apikey={TICKETMASTER_APIKEY}&keyword={keyword}'
#     response = requests.get(BASE_URL + query).json()

#     if '_embedded' in response and 'attractions' in response['_embedded']:
#         return response['_embedded']['attractions']
#     else:
#         return None


# def search_classifications(keyword):
#     query = f'classifications?apikey={TICKETMASTER_APIKEY}&keyword={keyword}'
#     response = requests.get(BASE_URL + query).json()

#     if '_embedded' in response and 'classifications' in response['_embedded']:
#         return response['_embedded']['classifications']
#     else:
#         return None


# def search_venues(keyword):
#     query = f'venues?apikey={TICKETMASTER_APIKEY}&keyword={keyword}'
#     response = requests.get(BASE_URL + query).json()

#     if '_embedded' in response and 'venues' in response['_embedded']:
#         return response['_embedded']['venues']
#     else:
#         return None

def extract_events_details(response):
    events_list = []

    if '_embedded' in response and 'events' in response['_embedded']:
        events = response['_embedded']['events']
        for index in range(len(events)):
            event_details = {}
            # Extract image URL
            event_details['image_url'] = events[index]['images'][0]['url']
            
            # Extract basic information
            event_details['name'] = events[index]['name']
            event_details['id'] = events[index]['id']
            event_details['url'] = events[index]['url']

            # Extract datetime
            event_details['event_date'] = events[index]['dates']['start']['localDate']
            event_details['event_time'] = events[index]['dates']['start'].get('localTime', '')

            # Extract city, country and venue
            event_details['city'] = events[index]['_embedded']['venues'][0]['city']['name']
            event_details['country'] = events[index]['_embedded']['venues'][0]['country']['name']
            event_details['venue_name'] = events[index]['_embedded']['venues'][0].get('name', '')

            # Extract price range (if available)
            if 'priceRanges' in events[index] and 'min' in events[index]['priceRanges'][0] and 'max' in events[index]['priceRanges'][0]:
                price_ranges = events[index]['priceRanges']
                event_details['price_range'] = f"{price_ranges[0].get('min', '')} - {price_ranges[0].get('max', '')} {price_ranges[0].get('currency', '')}"
            else:
                event_details['price_range'] = "N/A"
                
            events_list.append(event_details)

    return events_list


def get_events(genres=None, city=None, event_id_list=None):
    query = ''
    if event_id_list:
        query += f'&id={",".join(event_id_list)}'
    if city:
        query += f'&city={city.lower()}'
    if genres:
        query += f'&classificationName={(",").join(genres)}'
    print(BASE_URL + query)
    response = requests.get(BASE_URL + query).json()
    events_list = extract_events_details(response)

    return events_list
 