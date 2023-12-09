import psycopg2
import os

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOSTNAME = os.getenv("DB_HOSTNAME")
DB_PORT = os.getenv('DB_PORT')
DB = os.getenv('DB')


def db_connection():
    try:
        connection = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOSTNAME,
            port=DB_PORT,
            database=DB)
        print("Connected to PostgreSQL successfully!")
        return connection
    except psycopg2.Error as e:
        print(f"Error: Unable to connect to the database.\n{e}")
        return None


def execute_query(query, query_type='select'):
    try:
        connection = db_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)

            if query_type == 'select':
                result = cursor.fetchall()
                return result
            else:
                connection.commit()
            print(f"{query_type.capitalize()} query executed successfully!")
        if connection:
            connection.close()
            print("Connection closed.")
    except psycopg2.Error as e:
        if connection:
            connection.rollback()
        print(f"Error: Unable to execute the query.\n{e}")
