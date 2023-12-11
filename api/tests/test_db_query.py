import unittest
import os
import psycopg2
from unittest.mock import patch, MagicMock
from api.utils.db_query import db_connection, execute_query

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOSTNAME = os.getenv("DB_HOSTNAME")
DB_PORT = os.getenv('DB_PORT')
DB = os.getenv('DB')


class TestDatabaseFunctions(unittest.TestCase):

    @patch('psycopg2.connect')
    def test_db_connection_successful(self, mock_connect):
        # Mock a successful connection
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        # Call the function and check the result
        connection = db_connection()
        self.assertIsNotNone(connection)
        mock_connect.assert_called_once_with(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOSTNAME,
            port=DB_PORT,
            database=DB)
        mock_connection.close.assert_not_called()  # Connection should not be closed on success

    @patch('psycopg2.connect', side_effect=psycopg2.Error('Connection failed'))
    def test_db_connection_failure(self, mock_connect):
        # Mock a connection failure
        connection = db_connection()
        self.assertIsNone(connection)
        mock_connect.assert_called_once()

    @patch('api.utils.db_query.db_connection')
    def test_execute_query_select(self, mock_db_connection):
        # Mock a successful connection
        mock_connection = MagicMock()
        mock_db_connection.return_value = mock_connection

        # Mock a successful cursor
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        # Mock the fetchall result
        mock_cursor.fetchall.return_value = [('result',)]

        # Call the function and check the result
        result = execute_query('SELECT * FROM your_table', query_type='select')
        self.assertEqual(result, [('result',)])

        # Check that the cursor and connection methods were called
        mock_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with('SELECT * FROM your_table')
        mock_cursor.fetchall.assert_called_once()
        mock_connection.commit.assert_not_called()  # No commit for SELECT

    @patch('api.utils.db_query.db_connection')
    def test_execute_query_insert(self, mock_db_connection):
        # Mock a successful connection
        mock_connection = MagicMock()
        mock_db_connection.return_value = mock_connection

        # Mock a successful cursor
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        # Call the function and check the result
        execute_query('INSERT INTO your_table (column1, column2) VALUES (value1, value2)', query_type='insert')

        # Check that the cursor and connection methods were called
        mock_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with('INSERT INTO your_table (column1, column2) VALUES (value1, value2)')
        mock_cursor.fetchall.assert_not_called()  # No fetchall for INSERT
        mock_connection.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
