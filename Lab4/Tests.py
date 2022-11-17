
import requests
import unittest
from http.server import SimpleHTTPRequestHandler
from io import BytesIO as IO
from Server import Database, Lab4HTTPRequestHandler
from unittest.mock import MagicMock


from TwitterAPI import BEARER_TOKEN, TwitterAPI


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()

    def tearDown(self):
        self.db = None

    def test_load_tweets_returns_empty_list_on_error(self):
        self.db.tweets = 30
        self.assertTrue(type(self.db.load_tweets()) is list)
        self.assertEqual(self.db.load_tweets(), [])

    def test_can_load_tweets_default(self):
        self.assertEqual(self.db.load_tweets(), [])

    def test_can_load_tweets_mocked_db(self):
        self.db.tweets = [{"tweet1": "test"}, {"tweet2": "test"}]
        self.assertEqual(len(self.db.load_tweets()), 2)

    def test_can_save_tweets(self): # verifie si les tweets sont bien enregisté dans l base de donnée
        self.assertEqual(len(self.db.tweets), 0)
        self.db.save_tweets([{"tweet1": "test"}, {"tweet2": "test"}])
        self.assertEqual(len(self.db.tweets), 2)

    def test_save_invalid_tweets(self):
        self.assertEqual(len(self.db.tweets), 0)
        self.db.save_tweets(5)
        self.db.save_tweets("invalid tweet")
        self.assertEqual(len(self.db.tweets), 0)


class MockRequest(object):
    def makefile(self, *args, **kwargs):
        return IO(b"GET /")

    def sendall(self, *args, **kwargs):
        return


class MockServer(object):
    def __init__(self, ip_port, Handler):
        self.handler = Handler(MockRequest(), ip_port, self)


class TestServer(unittest.TestCase):
    def setUp(self):
        SimpleHTTPRequestHandler.do_GET = MagicMock(return_value=200)



    def test_route_invalid_path(self):
        self.server = MockServer(('0.0.0.0', 8888), Lab4HTTPRequestHandler)
        self.server.handler.path = "/fdsafdsa"
        self.server.handler.do_GET()
        self.assertEqual("Search.html", self.server.handler.path)

    def test_route_search(self):
        self.server = MockServer(('0.0.0.0', 8888), Lab4HTTPRequestHandler)
        self.server.handler.path = "/"
        self.server.handler.do_GET()
        self.assertEqual("Search.html", self.server.handler.path)



class TestTwitterAPI(unittest.TestCase):
    # header tests
    def test_request_no_header(self):
        headers = None
        url, params = TwitterAPI.create_twitter_url("data", 10)
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        self.assertEqual(json_response['error']['message'],
                         "Invalid 'headers': 'headers' must not be empty")

        # authorization tests

    def test_header_no_authorization(self):
        headers = {'Authorization': None}
        url, params = TwitterAPI.create_twitter_url("data", 10)
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        self.assertEqual(json_response['error']['message'],
                         "Invalid 'headers': 'Authorization' must not be None")


    def test_header_is_dictionary(self):
        headers = "not a dictionary"
        url, params = TwitterAPI.create_twitter_url("data", 10)
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        self.assertEqual(json_response['error']['message'],
                         "Invalid 'headers': 'headers' must not be a dictionary")



    def test_header_authorization_is_string(self):
        headers = {'Authorization': 0}
        url, params = TwitterAPI.create_twitter_url("data", 10)
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        self.assertEqual(json_response['error']['message'],
                         "Invalid 'headers': 'Authorization' must be a string")

    def test_header_empty_bearer_token(self):
        BEARER_TOKEN = ""
        headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}
        url, params = TwitterAPI.create_twitter_url("data", 10)
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        self.assertEqual(json_response['error']['message'],
                         "Invalid 'headers': 'Authorization' must have a bearer token")

    # url tests
    def test_no_url(self):
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url("data", 10)
        url = None
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        self.assertEqual(json_response['error']['message'],
                         "Invalid 'url': 'url' must not be None")

    def test_url_is_string(self):
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url("data", 10)
        url = 0
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        self.assertEqual(json_response['error']['message'],
                         "Invalid 'url': 'url' must be a string")

    def test_empty_url(self):
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url("data", 10)
        url = ""
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        self.assertEqual(json_response['error']['message'],
                         "Invalid 'url': 'url' must not be empty")

    # params tests
    def test_no_params(self):
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url("data", 10)
        params = None
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        self.assertEqual(json_response['error']['message'],
                         "Invalid 'params': 'params' must not be None")

    def test_params_is_dictionary(self):
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url("data", 10)
        params = "not a dictionary"
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        self.assertEqual(json_response['error']['message'],
                         "Invalid 'params': 'params' must be a dictionary")

    # query tests
    def test_no_query(self):
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url(None, 10)
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        self.assertEqual(json_response['error']['message'],
                         "Invalid 'params': 'query' must not be None")

    def test_query_is_string(self):
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url(0, 10)
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        self.assertEqual(json_response['error']['message'],
                         "Invalid 'params': 'query' must be a string")

    def test_empty_query(self):
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url("", 10)
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        self.assertEqual(json_response['error']['message'],
                         "Invalid 'params': 'query' must not be empty")

    # max results tests
    def test_no_max_results(self):
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url("data", None)
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        self.assertEqual(json_response['error']['message'],
                         "Invalid 'params': 'max_results' must not be None")

    def test_max_results_is_int(self):
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url("data", "not an int")
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        self.assertEqual(json_response['error']['message'],
                         "Invalid 'params': 'max_results' must be an int")

    def test_request_less_than_10_max_results(self):
        self.request = requests.request
        requests.request = MagicMock(
            return_value={'errors': [{'parameters': {'max_results': ['9']}, 'message': 'The `max_results` query parameter value [9] is not between 10 and 100'}], 'title': 'Invalid Request',
                          'detail': 'One or more parameters to your request was invalid.',
                          'type': 'https://api.twitter.com/2/problems/invalid-request'})
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url("data", 9)
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        self.assertEqual(json_response['error']['message'],
                         "Invalid 'params': 'max_results' must be between 10 and 100")
        requests.request = self.request

    def test_request_more_than_100_max_results(self):
        self.request = requests.request
        requests.request = MagicMock(
            return_value={'errors': [{'parameters': {'max_results': ['101']}, 'message': 'The `max_results` query parameter value [101] is not between 10 and 100'}], 'title':
                'Invalid Request', 'detail': 'One or more parameters to your request was invalid.',
                          'type': 'https://api.twitter.com/2/problems/invalid-request'})
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url("data", 101)
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        self.assertEqual(json_response['error']['message'],
                         "Invalid 'params': 'max_results' must be between 10 and 100")
        requests.request = self.request


if __name__ == '__main__':
    unittest.main()
