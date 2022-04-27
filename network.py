import socket
from urllib.parse import urlsplit
import ssl


class HTTPClient:
    @staticmethod
    def http_request(url, http_method, http_version, headers, sending_data):
        request = HTTPRequest(url, http_method, http_version, headers, sending_data)

        s = ssl.wrap_socket(socket.socket()) if request.port == 443 else socket.socket()

        try:
            s.connect((request.host, request.port))
        except OSError:
            print(f"Не удалось подключиться к сокету, данные:"
                  f"\n{url = }\n{http_method = }\n{request.host = }\n{request.port = }")

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
    def __init__(self, url, http_method, http_version, headers, sending_data):
        url_parts = urlsplit(url)
        self.path = url_parts.path if len(url_parts.path) == 0 or url_parts.path[0] != '/' else url_parts.path[1:]

        self.headers = headers.split(', ') if headers is not None else None

        self.host = url_parts.netloc if headers is None or 'Host:' not in headers else None

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
                'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0',
                'Connection: close'
            ]

            if self.http_method in ['POST', 'PUT'] and self.sending_data is not None:
                request_data.append(f'Content-Length: {len(self.sending_data.encode())}')
        else:
            request_data = [f'{self.http_method} /{self.path} HTTP/{self.http_version}']

            if self.host is not None:
                request_data += [f'Host: {self.host}']

            request_data += self.headers

            if self.http_method in ['POST', 'PUT'] \
                    and 'Content-Length' not in [x for x in self.sending_data.split(':')]:
                request_data.append(f'Content-Length: {len(self.sending_data.encode())}')

        request_data.append('\r\n')

        request = '\r\n'.join(request_data)

        if self.http_method in ['POST', 'PUT'] and self.sending_data is not None:
            return request + self.sending_data
        else:
            return request


class HTTPResponse:
    def __init__(self, decoded_response, bytes_response):
        self.decoded_response = decoded_response

        decoded_response = decoded_response.split('\r\n\r\n', 1)
        d_response = decoded_response[0].split('\r\n')

        self.inf = d_response[0]
        self.headers = {r.split(': ', 1)[0]: r.split(': ', 1)[1] for r in d_response[1:]}

        self.body = decoded_response[1] if len(decoded_response) == 2 else None
        self.bytes_response = bytes_response
