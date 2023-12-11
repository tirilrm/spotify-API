import unittest
from unittest.mock import patch, Mock
from api.utils.spotify_api import get_auth_header, get_spotify_id, get_top_artists_and_genres


class SpotifyAPITestCase(unittest.TestCase):

    @patch('requests.get')
    def test_get_auth_header(self, mock_requests_get):
        # Test get_auth_header function
        token = 'test_token'
        auth_header = get_auth_header(token)
        expected_header = {"Authorization": "Bearer " + token}
        self.assertEqual(auth_header, expected_header)

    @patch('requests.get')
    def test_get_spotify_id(self, mock_requests_get):
        # Test get_spotify_id function
        token = 'test_token'
        mock_response = Mock()
        mock_response.json.return_value = {'id': 'test_spotify_id'}
        mock_requests_get.return_value = mock_response

        spotify_id = get_spotify_id(token)
        self.assertEqual(spotify_id, 'test_spotify_id')

    @patch('requests.get')
    def test_get_top_artists_and_genres(self, mock_requests_get):
        # Test get_top_artists_and_genres function
        token = 'test_token'
        mock_response = Mock()
        mock_response.json.return_value = {
            'items': [
                {'name': 'Artist1', 'genres': ['Genre1', 'Genre2']},
                {'name': 'Artist2', 'genres': ['Genre2', 'Genre3']}
            ]
        }
        mock_requests_get.return_value = mock_response

        top_artists, top_genres = get_top_artists_and_genres(token)
        self.assertEqual(top_artists, ['Artist1', 'Artist2'])
        self.assertEqual(sorted(top_genres), sorted(['Genre1', 'Genre2', 'Genre3']))


if __name__ == '__main__':
    unittest.main()
