from flask import Flask, render_template, request
from api.utils.credentials import TICKETMASTER_APIKEY
import requests
import csv


app = Flask(__name__)


BASE_URL = 'https://app.ticketmaster.com/discovery/v2/'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search/events', methods=['POST'])
def search_events_route():
    keyword = request.form['event_keyword']
    event_results, event_data = search_events(keyword)
    return render_template('results.html', events=event_results, data=event_data)


@app.route('/search/attractions', methods=['POST'])
def search_attractions_route():
    keyword = request.form['attraction_keyword']
    attraction_results = search_attractions(keyword)
    return render_template('attractions_results.html', attractions=attraction_results)


@app.route('/search/classifications', methods=['POST'])
def search_classifications_route():
    keyword = request.form['classification_keyword']
    classification_results = search_classifications(keyword)
    return render_template('classifications_results.html', classifications=classification_results)


@app.route('/search/venues', methods=['POST'])
def search_venues_route():
    keyword = request.form['venue_keyword']
    venue_results = search_venues(keyword)
    return render_template('results.html', venues=venue_results)


def search_events(keyword):
    query = f'events?apikey={TICKETMASTER_APIKEY}&keyword={keyword}'
    response = requests.get(BASE_URL + query).json()
    # print(response)
    if '_embedded' in response and 'events' in response['_embedded']:
        events = response['_embedded']['events']

        # Extract and write to CSV
        data = []
        with open('events.csv', 'w', newline='') as file:
            writer = csv.writer(file)

            # Write CSV header
            writer.writerow(['Name', 'ID', 'Locale', 'Genres', 'SubGenres', 'Segments', 'Venue', 'Attraction',
                             'VenueType', 'PostalCode', 'Address', 'ImageURL', 'ImageWidth', 'ImageHeight'])

            for event in events:
                name = event.get('name', '')
                event_id = event.get('id', '')
                locale = event.get('locale', '')

                # Extract genre, sub_genre, and segment from all classifications
                genres = []
                sub_genres = []
                segments = []

                # print(event.keys())

                if 'classifications' in event.keys():
                    for classification in event['classifications']:
                        # Extracting information from the primary segment
                        segment_name = classification.get('segment', {}).get('name', '')
                        segments.append(segment_name)

                        # Extracting information from the primary genre
                        genre_name = classification.get('genre', {}).get('name', '')
                        genres.append(genre_name)

                        # Extracting information from the tertiary sub-genre
                        sub_genre_name = classification.get('subGenre', {}).get('name', '')
                        sub_genres.append(sub_genre_name)

                # Use a delimiter (e.g., comma) to join multiple values into a single string
                segment = ', '.join(segments)
                genre = ', '.join(genres)
                sub_genre = ', '.join(sub_genres)
                venue_name = ''
                if '_embedded' in event and 'venues' in event['_embedded'] and event['_embedded']['venues']:
                    venue_name = event['_embedded']['venues'][0]['name'] if 'name' in event['_embedded']['venues'][0] else ''

                attraction_name = ''
                if '_embedded' in event and 'attractions' in event['_embedded'] and event['_embedded']['attractions']:
                    attraction_name = event['_embedded']['attractions'][0]['name'] if 'name' in event['_embedded']['attractions'][0] else ''

                # Extract venue information
                venue_info = event['_embedded']['venues'][0] if '_embedded' in event and 'venues' in event['_embedded'] and event['_embedded']['venues'] else {}
                venue_type = venue_info.get('type', '')
                postal_code = venue_info.get('postalCode', '')
                address = venue_info.get('address', '')

                # Extract image information
                image_info = event.get('images', [{}])[0]
                image_url = image_info.get('url', '')
                image_width = image_info.get('width', '')
                image_height = image_info.get('height', '')

                # Write to CSV
                writer.writerow([name, event_id, locale, genre, sub_genre, segment, venue_name, attraction_name,
                                 venue_type, postal_code, address, image_url, image_width, image_height])

                data.append({
                    'EventName': name,
                    'EventID': event_id,
                    'Genre': genre,
                    'SubGenre': sub_genre,
                    'Segment': segment,
                    'Venue': venue_name,
                    'Attraction': attraction_name,
                    'VenueType': venue_type,
                    'PostalCode': postal_code,
                    'Address': address,
                    'ImageURL': image_url,
                    'ImageWidth': image_width,
                    'ImageHeight': image_height
                })

        return events, data
    else:
        return None


def search_attractions(keyword):
    query = f'attractions?apikey={TICKETMASTER_APIKEY}&keyword={keyword}'
    response = requests.get(BASE_URL + query).json()

    if '_embedded' in response and 'attractions' in response['_embedded']:
        return response['_embedded']['attractions']
    else:
        return None


def search_classifications(keyword):
    query = f'classifications?apikey={TICKETMASTER_APIKEY}&keyword={keyword}'
    response = requests.get(BASE_URL + query).json()

    if '_embedded' in response and 'classifications' in response['_embedded']:
        return response['_embedded']['classifications']
    else:
        return None


def search_venues(keyword):
    query = f'venues?apikey={TICKETMASTER_APIKEY}&keyword={keyword}'
    response = requests.get(BASE_URL + query).json()

    if '_embedded' in response and 'venues' in response['_embedded']:
        return response['_embedded']['venues']
    else:
        return None


def get_events_based_on_genre(genres : list, city : str):
    query = f'events?apikey={TICKETMASTER_APIKEY}&locale=*&city={city.lower()}&classificationName={(",").join(genres)}'

    response = requests.get(BASE_URL + query).json()['_embedded']['events']
    events_list = []
    for i in range(len(response)):
        events_list.append({key: response[i][key] for key in ['name', 'id']})
    return events_list

if __name__ == '__main__':
    app.run(debug=True, port=5001)
