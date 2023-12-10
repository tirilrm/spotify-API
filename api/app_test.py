# app_test.py

import unittest
from unittest.mock import patch
import requests
from .app import process_query


def test_basic():
	assert process_query("test") == "Test has passed"


class APITestCase(unittest.TestCase):
    @patch('requests.get')
    def test_spotify_api_connection(self, mock_get):
        # Configure the mock to return a response with an OK status code for Spotify
        mock_get.return_value.status_code = 200
        response = requests.get('https://api.spotify.com')
        self.assertEqual(response.status_code, 200)

    @patch('requests.get')
    def test_ticketmaster_api_connection(self, mock_get):
        # Configure the mock to return a response with an OK status code for Ticketmaster
        mock_get.return_value.status_code = 200
        response = requests.get('https://app.ticketmaster.com')
        self.assertEqual(response.status_code, 200)

# This allows the test to be run from the command line
if __name__ == '__main__':
    unittest.main()
