import requests
import os

TICKETMASTER_APIKEY = os.getenv('TICKETMASTER_APIKEY')

BASE_URL = f'https://app.ticketmaster.com/discovery/v2/events?apikey={TICKETMASTER_APIKEY}&locale=*'


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
