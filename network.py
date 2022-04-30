import socket
import ssl
from urllib.parse import urlsplit


class HTTPClient:
    user_agents = {
        'Chrome': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) '
                  'AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
        'Firefox': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) '
                   'Gecko/20100101 Firefox/101.0',
        'Edge': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582',
        'Opera': 'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) '
                 'Presto/2.12.388 Version/12.16.2'
    }

    @staticmethod
    def http_request(url, http_method, http_version, headers,
                     sending_data, user_agent):
        request = HTTPRequest(url,
                              http_method,
                              http_version,
                              headers,
                              sending_data,
                              user_agent)

        if request.port == 443:
            s = ssl.wrap_socket(socket.socket())
        else:
            s = socket.socket()

        s.connect((request.host, request.port))

        s.sendall(str(request).encode())

        data = s.recv(512)
        response = bytearray(data)

        while True:
            if not data:
                break
            data = s.recv(512)
            response.extend(data)

        s.close()

        bytes_response = bytes(response)
        decoded_response = bytes(response).decode(errors='ignore')

        return HTTPResponse(decoded_response, bytes_response)


class HTTPRequest:
    def __init__(self, url, http_method, http_version, headers,
                 sending_data, user_agent):
        url_parts = urlsplit(url)

        if len(url_parts.path) == 0 or url_parts.path[0] != '/':
            self.path = url_parts.path
        else:
            self.path = url_parts.path[1:]

        self.headers = headers.split(', ') if headers is not None else None

        if headers is None or 'Host:' not in headers:
            self.host = url_parts.netloc
        else:
            self.host = None

        if user_agent is not None \
                and (headers is None or 'User-Agent:' not in headers):
            self.user_agent = HTTPClient.user_agents[user_agent]
        else:
            self.user_agent = None

        if url_parts.scheme not in ('http', 'https'):
            raise ValueError(f'Incorrect url {url}, expected http or https')

        self.port = 80 if url_parts.scheme == 'http' else 443

        self.http_method = http_method
        self.http_version = http_version
        self.sending_data = sending_data

    def __str__(self):
        if self.headers is None:
            request_data = [
                f'{self.http_method} /{self.path} HTTP/{self.http_version}',
                f'Host: {self.host}',
                'Connection: close'
            ]

            if self.user_agent is not None:
                request_data += [f'User-Agent: {self.user_agent}']

            if self.http_method in ['POST', 'PUT'] \
                    and self.sending_data is not None:
                content_length = len(self.sending_data.encode())
                request_data.append(f'Content-Length: {content_length}')
        else:
            first_http_line = f'{self.http_method} /{self.path} ' \
                              f'HTTP/{self.http_version}'
            request_data = [first_http_line]

            if self.host is not None:
                request_data += [f'Host: {self.host}']

            if self.user_agent is not None:
                request_data += [f'User-Agent: {self.user_agent}']

            request_data += self.headers

            headers_keys = [x.split(':')[0] for x in self.headers]

            if self.http_method in ['POST', 'PUT'] \
                    and 'Content-Length' not in headers_keys:
                content_length = len(self.sending_data.encode())
                request_data.append(f'Content-Length: {content_length}')

        request_data.append('\r\n')

        request = '\r\n'.join(request_data)

        if self.http_method in ['POST', 'PUT'] \
                and self.sending_data is not None:
            return request + self.sending_data
        else:
            return request


class HTTPResponse:
    def __init__(self, decoded_response, bytes_response):
        self.decoded_response = decoded_response

        decoded_response = decoded_response.split('\r\n\r\n', 1)
        d_response = decoded_response[0].split('\r\n')

        self.inf = d_response[0]

        self.headers = {}
        for r in d_response[1:]:
            header_with_value = r.split(': ', 1)
            self.headers[header_with_value[0]] = header_with_value[1]

        if len(decoded_response) == 2:
            self.body = decoded_response[1]
        else:
            self.body = None

        self.bytes_response = bytes_response
