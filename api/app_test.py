# app_test.py


from .app import process_query


def test_basic():
	assert process_query("test") == "Test has passed"
