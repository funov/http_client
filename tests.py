import os.path
import unittest
from unittest.mock import patch, mock_open
import utils
import html_parser
from network import HTTPRequest, HTTPResponse


class GETRequestTests(unittest.TestCase):
    def setUp(self):
        self.request1 = HTTPRequest(
            "https://example.com",
            "GET",
            1.1,
            None,
            None,
            'Firefox')
        self.request2 = HTTPRequest(
            "https://example.com",
            "GET",
            1.1,
            "Connection: Keep-Alive",
            None,
            None)
        self.request3 = HTTPRequest(
            "https://example.com",
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
        self.request1 = HTTPRequest(
            "https://example.com",
            "POST",
            1.1,
            None,
            "Test message",
            'Firefox')
        self.request2 = HTTPRequest(
            "https://example.com",
            "POST",
            1.1,
            "Connection: Keep-Alive, "
            "Accept-Language: fr",
            "Test message",
            None)
        self.request3 = HTTPRequest(
            "https://example.com",
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
        self.request1 = HTTPRequest(
            "https://example.com",
            "HEAD",
            1.1,
            None,
            None,
            'Firefox')
        self.request2 = HTTPRequest(
            "https://example.com",
            "HEAD",
            1.1,
            "Connection: Keep-Alive, "
            "Accept-Language: fr",
            None,
            None)
        self.request3 = HTTPRequest(
            "https://example.com",
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
        self.request1 = HTTPRequest(
            "https://example.com",
            "PUT",
            1.1,
            None,
            "Test message",
            'Firefox')
        self.request2 = HTTPRequest(
            "https://example.com",
            "PUT",
            1.1,
            "Connection: Keep-Alive, "
            "Accept-Language: fr",
            "Test message",
            None)
        self.request3 = HTTPRequest(
            "https://example.com",
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


class HTTPResponseTests(unittest.TestCase):
    def setUp(self):
        self.expected_decoded_response = 'HTTP/1.1 200 OK\r\nDate: Mon, 27 Jul 2009 ' \
                                '12:28:53 GMT\r\nServer: Apache/2.2.14 ' \
                                '(Win32)\r\nLast-Modified: Wed, 22 Jul ' \
                                '2009 19:15:56 GMT\r\nContent-Length: 88' \
                                '\r\nContent-Type: text/html\r\n' \
                                'Connection: Closed\r\n\r\n<!doctype html>' \
                                '\r\n<html>\r\n<body>\r\n<h1>Hello, ' \
                                'World!</h1>\r\n</body>\r\n</html>'
        self.expected_bytes_response = self.expected_decoded_response.encode()
        self.expected_information = "HTTP/1.1 200 OK"
        self.expected_headers_dict = {
            'Date': 'Mon, 27 Jul 2009 12:28:53 GMT',
            'Server': 'Apache/2.2.14 (Win32)',
            'Last-Modified': 'Wed, 22 Jul 2009 19:15:56 GMT',
            'Content-Length': '88',
            'Content-Type': 'text/html',
            'Connection': 'Closed'
        }
        self.expected_body = '<!doctype html>\r\n<html>\r\n<body>\r\n' \
                             '<h1>Hello, World!</h1>\r\n</body>\r\n</html>'
        self.expected_head = 'HTTP/1.1 200 OK\r\nDate: Mon, 27 Jul 2009 ' \
                             '12:28:53 GMT\r\nServer: Apache/2.2.14 ' \
                             '(Win32)\r\nLast-Modified: Wed, 22 Jul ' \
                             '2009 19:15:56 GMT\r\nContent-Length: 88' \
                             '\r\nContent-Type: text/html\r\n' \
                             'Connection: Closed'

        self.response = HTTPResponse(self.expected_decoded_response, self.expected_bytes_response)

    def test_decoded_response(self):
        self.assertEqual(self.expected_decoded_response, self.response.decoded_response)

    def test_bytes_response(self):
        self.assertEqual(self.expected_bytes_response, self.response.bytes_response)

    def test_information(self):
        self.assertEqual(self.expected_information, self.response.information)

    def test_headers_dict(self):
        self.assertEqual(self.expected_headers_dict, self.response.headers_dict)

    def test_body(self):
        self.assertEqual(self.expected_body, self.response.body)

    def test_head(self):
        self.assertEqual(self.expected_head, self.response.head)


class HTMLParserTests(unittest.TestCase):
    def setUp(self):
        self.html = '<!doctype html>\r\n<html>\r\n<body>\r\n' \
                    '<img src="http://python.org" alt="some text2">' \
                    '\r\n<h1>Hello, World!</h1>\r\n' \
                    '<img src="http://example.com" alt="some text1">' \
                    '\r\n</body>\r\n</html>'
        self.expected_result = ['http://python.org', 'http://example.com']

    def test_basic_html(self):
        image_links = html_parser.get_image_links_from_html(self.html)

        self.assertEqual(self.expected_result, image_links)


class UtilsTests(unittest.TestCase):
    def setUp(self):
        self.expected1 = b'efg'

        head2 = 'HTTP/1.1 200 OK\r\nDate: Mon, 27 Jul 2009 ' \
                '12:28:53 GMT\r\nServer: Apache/2.2.14 ' \
                '(Win32)\r\nLast-Modified: Wed, 22 Jul ' \
                '2009 19:15:56 GMT\r\nContent-Length: 6' \
                '\r\nContent-Type: image\r\n' \
                'Connection: Closed\r\n\r\n'
        image2 = '123efg'
        decoded_response2 = head2 + image2
        self.response2 = HTTPResponse(decoded_response2, decoded_response2.encode())
        self.expected_write_data2 = [head2[:-4], image2.encode()]
        self.expected_folder_info2 = [(os.path.join('folder_name', 'headers.txt'), 'w'), (os.path.join('folder_name', 'some_image.png'), 'wb')]

        self.image_name_to_image_bytes = {
            "image1.png": b'1234',
            "image2.png": b'abc',
            "image3.png": b'1bc'
        }
        self.expected_write_data3 = [b'1234', b'abc', b'1bc']
        self.expected_folder_info3 = [
            (os.path.join('folder_name', 'image', 'image1.png'), 'wb'),
            (os.path.join('folder_name', 'image', 'image2.png'), 'wb'),
            (os.path.join('folder_name', 'image', 'image3.png'), 'wb')]

    def test_get_image_bytes(self):
        headers = {'Content-Length': 3}
        actual = utils.get_image_bytes(b'abcdefg', headers)

        self.assertEqual(self.expected1, actual)

    def test_write_one_image_response(self):
        m = mock_open()
        with patch('utils.open', m):
            utils.write_one_image_response('folder_name', self.response2, 'https://some_image.png')

        folder_info, write_data = UtilsTests.get_info(m)

        self.assertEqual(self.expected_write_data2, write_data)
        self.assertEqual(self.expected_folder_info2, folder_info)

    def test_write_all_images(self):
        m = mock_open()

        with patch('utils.open', m):
            utils.write_all_images('folder_name', self.image_name_to_image_bytes)

        folder_info, write_data = UtilsTests.get_info(m)

        self.assertEqual(self.expected_write_data3, write_data)
        self.assertEqual(self.expected_folder_info3, folder_info)

    @staticmethod
    def get_info(m):
        calls = m.mock_calls

        folder_info = []
        write_data = []
        for call in calls:
            if call[0] == '().write':
                write_data.append(call[1][0])
            if call[0] == '':
                folder_info.append(call[1])

        return folder_info, write_data
