import unittest
from unittest.mock import patch, Mock
from api.utils.ticketmaster_api import get_events, extract_events_details


class TestTicketMasterAPI(unittest.TestCase):

    @patch('requests.get')
    def test_extract_events_details(self, mock_requests_get):
        # Mock response data for events
        mock_response_data = {
            '_embedded': {
                'events': [
                    {
                        'name': 'Event1',
                        'id': '123',
                        'url': 'http://example.com/event1',
                        'images': [{'url': 'http://example.com/image1.jpg'}],
                        'dates': {'start': {'localDate': '2023-01-01', 'localTime': '18:00'}},
                        '_embedded': {
                            'venues': [
                                {'city': {'name': 'City1'}, 'country': {'name': 'Country1'}, 'name': 'Venue1'}
                            ]
                        }
                    }
                ]
            }
        }

        # Set up the mock response
        mock_requests_get.return_value = Mock(json=lambda: mock_response_data)

        # Call the function and check the extracted details
        events_list = extract_events_details(mock_response_data)
        expected_event_details = [
            {
                'name': 'Event1',
                'id': '123',
                'url': 'http://example.com/event1',
                'image_url': 'http://example.com/image1.jpg',
                'event_date': '2023-01-01',
                'event_time': '18:00',
                'city': 'City1',
                'country': 'Country1',
                'venue_name': 'Venue1',
                'price_range': 'N/A'
            }
        ]
        self.assertEqual(events_list, expected_event_details)

    @patch('requests.get')
    def test_get_events(self, mock_requests_get):
        # Mock response data for events
        mock_response_data = {
            '_embedded': {
                'events': [
                    {
                        'name': 'Event1',
                        'id': '123',
                        'url': 'http://example.com/event1',
                        'images': [{'url': 'http://example.com/image1.jpg'}],
                        'dates': {'start': {'localDate': '2023-01-01', 'localTime': '18:00'}},
                        '_embedded': {
                            'venues': [
                                {'city': {'name': 'City1'}, 'country': {'name': 'Country1'}, 'name': 'Venue1'}
                            ]
                        }
                    }
                ]
            }
        }

        # Set up the mock response
        mock_requests_get.return_value = Mock(json=lambda: mock_response_data)

        # Call the function and check the result
        events_list = get_events(city='City1')
        expected_event_details = [
            {
                'name': 'Event1',
                'id': '123',
                'url': 'http://example.com/event1',
                'image_url': 'http://example.com/image1.jpg',
                'event_date': '2023-01-01',
                'event_time': '18:00',
                'city': 'City1',
                'country': 'Country1',
                'venue_name': 'Venue1',
                'price_range': 'N/A'
            }
        ]
        self.assertEqual(events_list, expected_event_details)


if __name__ == '__main__':
    unittest.main()
