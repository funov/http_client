import unittest
from network import HTTPRequest


class GETRequestTests(unittest.TestCase):
    def setUp(self):
        self.request1 = HTTPRequest("https://example.com",
                                    "GET",
                                    1.1,
                                    None,
                                    None,
                                    'Firefox')
        self.request2 = HTTPRequest("https://example.com",
                                    "GET",
                                    1.1,
                                    "Connection: Keep-Alive",
                                    None,
                                    None)
        self.request3 = HTTPRequest("https://example.com",
                                    "GET",
                                    1.1,
                                    None,
                                    "Test message",
                                    'Firefox')

        self.expected_result1 = 'GET / HTTP/1.1\r\nHost: example.com\r\n' \
                                'Connection: close\r\n' \
                                'User-Agent: Mozilla/5.0 (Macintosh; ' \
                                'Intel Mac OS X 10.15; rv:101.0) ' \
                                'Gecko/20100101 Firefox/101.0\r\n\r\n'
        self.expected_result2 = 'GET / HTTP/1.1\r\nHost: example.com\r\n' \
                                'Connection: Keep-Alive\r\n\r\n'
        self.expected_result3 = 'GET / HTTP/1.1\r\nHost: example.com\r\n' \
                                'Connection: close\r\n' \
                                'User-Agent: Mozilla/5.0 (Macintosh; ' \
                                'Intel Mac OS X 10.15; rv:101.0) ' \
                                'Gecko/20100101 Firefox/101.0\r\n\r\n'

    def test_default_headers(self):
        result1 = str(self.request1)

        self.assertEqual(self.expected_result1, result1)

    def test_headers_from_user(self):
        result2 = str(self.request2)

        self.assertEqual(self.expected_result2, result2)

    def test_ignore_send_data_in_get(self):
        result3 = str(self.request3)

        self.assertEqual(self.expected_result3, result3)


class POSTRequestTests(unittest.TestCase):
    def setUp(self):
        self.request1 = HTTPRequest("https://example.com",
                                    "POST",
                                    1.1,
                                    None,
                                    "Test message",
                                    'Firefox')
        self.request2 = HTTPRequest("https://example.com",
                                    "POST",
                                    1.1,
                                    "Connection: Keep-Alive, "
                                    "Accept-Language: fr",
                                    "Test message",
                                    None)
        self.request3 = HTTPRequest("https://example.com",
                                    "POST",
                                    1.1,
                                    None,
                                    None,
                                    'Firefox')

        self.expected_result1 = 'POST / HTTP/1.1\r\nHost: example.com\r\n' \
                                'Connection: close\r\n' \
                                'User-Agent: Mozilla/5.0 (Macintosh; ' \
                                'Intel Mac OS X 10.15; rv:101.0) ' \
                                'Gecko/20100101 Firefox/101.0\r\n' \
                                'Content-Length: 12\r\n\r\nTest message'
        self.expected_result2 = 'POST / HTTP/1.1\r\nHost: example.com\r\n' \
                                'Connection: Keep-Alive' \
                                '\r\nAccept-Language: fr\r\n' \
                                'Content-Length: 12\r\n\r\nTest message'
        self.expected_result3 = 'POST / HTTP/1.1\r\nHost: example.com\r\n' \
                                'Connection: close\r\n' \
                                'User-Agent: Mozilla/5.0 (Macintosh; ' \
                                'Intel Mac OS X 10.15; rv:101.0) ' \
                                'Gecko/20100101 Firefox/101.0\r\n\r\n'

    def test_default_headers(self):
        result1 = str(self.request1)

        self.assertEqual(self.expected_result1, result1)

    def test_headers_from_user(self):
        result2 = str(self.request2)

        self.assertEqual(self.expected_result2, result2)

    def test_default_headers_without_send_data(self):
        result3 = str(self.request3)

        self.assertEqual(self.expected_result3, result3)


class HEADRequestTests(unittest.TestCase):
    def setUp(self):
        self.request1 = HTTPRequest("https://example.com",
                                    "HEAD",
                                    1.1,
                                    None,
                                    None,
                                    'Firefox')
        self.request2 = HTTPRequest("https://example.com",
                                    "HEAD",
                                    1.1,
                                    "Connection: Keep-Alive, "
                                    "Accept-Language: fr",
                                    None,
                                    None)
        self.request3 = HTTPRequest("https://example.com",
                                    "HEAD",
                                    1.1,
                                    None,
                                    "Test message",
                                    'Firefox')

        self.expected_result1 = 'HEAD / HTTP/1.1\r\nHost: example.com\r\n' \
                                'Connection: close\r\n' \
                                'User-Agent: Mozilla/5.0 (Macintosh; ' \
                                'Intel Mac OS X 10.15; rv:101.0) ' \
                                'Gecko/20100101 Firefox/101.0\r\n\r\n'
        self.expected_result2 = 'HEAD / HTTP/1.1\r\nHost: example.com\r\n' \
                                'Connection: Keep-Alive' \
                                '\r\nAccept-Language: fr\r\n\r\n'
        self.expected_result3 = 'HEAD / HTTP/1.1\r\nHost: example.com\r\n' \
                                'Connection: close\r\n' \
                                'User-Agent: Mozilla/5.0 (Macintosh; ' \
                                'Intel Mac OS X 10.15; rv:101.0) ' \
                                'Gecko/20100101 Firefox/101.0\r\n\r\n'

    def test_default_headers(self):
        result1 = str(self.request1)

        self.assertEqual(self.expected_result1, result1)

    def test_headers_from_user(self):
        result2 = str(self.request2)

        self.assertEqual(self.expected_result2, result2)

    def test_ignore_send_data_in_head(self):
        result3 = str(self.request3)

        self.assertEqual(self.expected_result3, result3)


class PUTRequestTests(unittest.TestCase):
    def setUp(self):
        self.request1 = HTTPRequest("https://example.com",
                                    "PUT",
                                    1.1,
                                    None,
                                    "Test message",
                                    'Firefox')
        self.request2 = HTTPRequest("https://example.com",
                                    "PUT",
                                    1.1,
                                    "Connection: Keep-Alive, "
                                    "Accept-Language: fr",
                                    "Test message",
                                    None)
        self.request3 = HTTPRequest("https://example.com",
                                    "PUT",
                                    1.1,
                                    None,
                                    None,
                                    'Firefox')

        self.expected_result1 = 'PUT / HTTP/1.1\r\nHost: example.com\r\n' \
                                'Connection: close\r\n' \
                                'User-Agent: Mozilla/5.0 (Macintosh; ' \
                                'Intel Mac OS X 10.15; rv:101.0) ' \
                                'Gecko/20100101 Firefox/101.0\r\n' \
                                'Content-Length: 12\r\n\r\nTest message'
        self.expected_result2 = 'PUT / HTTP/1.1\r\nHost: example.com\r\n' \
                                'Connection: Keep-Alive' \
                                '\r\nAccept-Language: fr\r\n' \
                                'Content-Length: 12\r\n\r\nTest message'
        self.expected_result3 = 'PUT / HTTP/1.1\r\nHost: example.com\r\n' \
                                'Connection: close\r\n' \
                                'User-Agent: Mozilla/5.0 (Macintosh; ' \
                                'Intel Mac OS X 10.15; rv:101.0) ' \
                                'Gecko/20100101 Firefox/101.0\r\n\r\n'

    def test_default_headers(self):
        result1 = str(self.request1)

        self.assertEqual(self.expected_result1, result1)

    def test_headers_from_user(self):
        result2 = str(self.request2)

        self.assertEqual(self.expected_result2, result2)

    def test_default_headers_without_send_data(self):
        result3 = str(self.request3)

        self.assertEqual(self.expected_result3, result3)
