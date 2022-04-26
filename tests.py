import unittest
from network import HTTPRequest


class GETRequestTests(unittest.TestCase):
    def setUp(self):
        self.request1 = HTTPRequest("https://example.com", "GET", 1.1, None, None)
        self.request2 = HTTPRequest("https://example.com", "GET", 1.1, "Connection: Keep-Alive", None)
        self.request3 = HTTPRequest("https://example.com", "GET", 1.1, None, "Test message")

        self.expected_result1 = 'GET / HTTP/1.1\r\nHost: example.com\r\nUser-Agent: ' \
                                'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0\r\n' \
                                'Connection: close\r\n\r\n'
        self.expected_result2 = 'GET / HTTP/1.1\r\nHost: example.com\r\nConnection: Keep-Alive\r\n\r\n'
        self.expected_result3 = 'GET / HTTP/1.1\r\nHost: example.com\r\nUser-Agent: ' \
                                'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0\r\n' \
                                'Connection: close\r\n\r\n'

    def test_default_headers(self):
        result1 = str(self.request1)

        self.assertEqual(result1, self.expected_result1)

    def test_headers_from_user(self):
        result2 = str(self.request2)

        self.assertEqual(result2, self.expected_result2)

    def test_ignore_send_data_in_get(self):
        result3 = str(self.request3)

        self.assertEqual(result3, self.expected_result3)


class POSTRequestTests(unittest.TestCase):
    def setUp(self):
        self.request1 = HTTPRequest("https://example.com", "POST", 1.1, None, "Test message")
        self.request2 = HTTPRequest("https://example.com", "POST", 1.1, "Connection: Keep-Alive, Accept-Language: fr",
                                    "Test message")
        self.request3 = HTTPRequest("https://example.com", "POST", 1.1, None, None)

        self.expected_result1 = 'POST / HTTP/1.1\r\nHost: example.com\r\nUser-Agent: ' \
                                'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0\r\n' \
                                'Connection: close\r\nContent-Length: 12\r\n\r\nTest message'
        self.expected_result2 = 'POST / HTTP/1.1\r\nHost: example.com\r\nConnection: Keep-Alive' \
                                '\r\nAccept-Language: fr\r\nContent-Length: 12\r\n\r\nTest message'
        self.expected_result3 = 'POST / HTTP/1.1\r\nHost: example.com\r\nUser-Agent: ' \
                                'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0\r\n' \
                                'Connection: close\r\n\r\n'

    def test_default_headers(self):
        result1 = str(self.request1)

        self.assertEqual(result1, self.expected_result1)

    def test_headers_from_user(self):
        result2 = str(self.request2)

        self.assertEqual(result2, self.expected_result2)

    def test_default_headers_without_send_data(self):
        result3 = str(self.request3)

        self.assertEqual(result3, self.expected_result3)


class HEADRequestTests(unittest.TestCase):
    def setUp(self):
        self.request1 = HTTPRequest("https://example.com", "HEAD", 1.1, None, None)
        self.request2 = HTTPRequest("https://example.com", "HEAD", 1.1, "Connection: Keep-Alive, "
                                                                        "Accept-Language: fr", None)
        self.request3 = HTTPRequest("https://example.com", "HEAD", 1.1, None, "Test message")

        self.expected_result1 = 'HEAD / HTTP/1.1\r\nHost: example.com\r\nUser-Agent: ' \
                                'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0\r\n' \
                                'Connection: close\r\n\r\n'
        self.expected_result2 = 'HEAD / HTTP/1.1\r\nHost: example.com\r\nConnection: Keep-Alive' \
                                '\r\nAccept-Language: fr\r\n\r\n'
        self.expected_result3 = 'HEAD / HTTP/1.1\r\nHost: example.com\r\nUser-Agent: ' \
                                'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0\r\n' \
                                'Connection: close\r\n\r\n'

    def test_default_headers(self):
        result1 = str(self.request1)

        self.assertEqual(result1, self.expected_result1)

    def test_headers_from_user(self):
        result2 = str(self.request2)

        self.assertEqual(result2, self.expected_result2)

    def test_ignore_send_data_in_head(self):
        result3 = str(self.request3)

        self.assertEqual(result3, self.expected_result3)


class PUTRequestTests(unittest.TestCase):
    def setUp(self):
        self.request1 = HTTPRequest("https://example.com", "PUT", 1.1, None, "Test message")
        self.request2 = HTTPRequest("https://example.com", "PUT", 1.1, "Connection: Keep-Alive, Accept-Language: fr",
                                    "Test message")
        self.request3 = HTTPRequest("https://example.com", "PUT", 1.1, None, None)

        self.expected_result1 = 'PUT / HTTP/1.1\r\nHost: example.com\r\nUser-Agent: ' \
                                'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0\r\n' \
                                'Connection: close\r\nContent-Length: 12\r\n\r\nTest message'
        self.expected_result2 = 'PUT / HTTP/1.1\r\nHost: example.com\r\nConnection: Keep-Alive' \
                                '\r\nAccept-Language: fr\r\nContent-Length: 12\r\n\r\nTest message'
        self.expected_result3 = 'PUT / HTTP/1.1\r\nHost: example.com\r\nUser-Agent: ' \
                                'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0\r\n' \
                                'Connection: close\r\n\r\n'

    def test_default_headers(self):
        result1 = str(self.request1)

        self.assertEqual(result1, self.expected_result1)

    def test_headers_from_user(self):
        result2 = str(self.request2)

        self.assertEqual(result2, self.expected_result2)

    def test_default_headers_without_send_data(self):
        result3 = str(self.request3)

        self.assertEqual(result3, self.expected_result3)
