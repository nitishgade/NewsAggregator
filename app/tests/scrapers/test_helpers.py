import pytest
from scrapers.helpers import get_article_content

'''
Unit test for the get_article_content function in helpers.py. Uses pytest and pytest-mock to mock the requests.get function and test when we get a successful response.
'''
def test_get_article_content_success(mocker):
	mock_response = mocker.Mock()
	mock_response.status_code = 200
	mock_response.text = "<html><head><title>Test Title</title></head><body>Main Content</body></html>"
	
	mocker.patch("scrapers.helpers.requests.get", return_value=mock_response)
	
	title, content = get_article_content("https://example.com")
	assert title == "Test Title"
	assert "Main Content" in content


'''
Unit test for get_article_content when the response status code is not 200. We expect to get a failure message.
'''
def test_get_article_content_bad_status(mocker):
	mock_response = mocker.Mock()
	mock_response.status_code = 404
	mocker.patch("scrapers.helpers.requests.get", return_value=mock_response)
	
	result = get_article_content("https://example.com")
	assert "Failed with status: 404" in result


'''
Unit test for get_article_content when there is an exception during the request. We expect to get an error message containing the exception details.
'''
def test_get_article_content_exception(mocker):
	mocker.patch("scrapers.helpers.requests.get", side_effect=Exception("Connection Timeout"))
	
	result = get_article_content("https://example.com")
	assert "Error is Connection Timeout" in result


