import argparse


def create_parser():
    parser = argparse.ArgumentParser(description="http-client, реализовано GET, POST, HEAD, PUT, "
                                                 "по GET запросу получает html и картинки")

    parser.add_argument('url', help='URL для HTTP запроса', type=str)
    parser.add_argument('http_method', help='Метод HTTP запроса (GET, POST, HEAD или PUT)', type=str)
    parser.add_argument('--http_version',
                        '-v',
                        help='Версия HTTP протокола (1.0 или 1.1), если не указать будет использована 1.1',
                        type=float,
                        choices=[1.0, 1.1],
                        default=1.1)
    parser.add_argument('--headers',
                        '-he',
                        help='Заголовки для HTTP запроса в формате: "Host: developer.mozilla.org, '
                             'Accept-Language: fr". Если не указать будут использованы стандартные: '
                             'Host: {будет взят из URL}; User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) '
                             'Gecko/20100101 Firefox/47.0; Connection: close',
                        type=str,
                        default=None)
    parser.add_argument('--send_dt',
                        '-d',
                        help='Данные для отправки по HTTP, только для POST или PUT, отправлять в формате "data"',
                        type=str,
                        default=None)

    return parser


def write_image(path, bytes_response, all_bytes_count, headers_bytes_count):
    with open(path, 'wb') as f:
        f.write(bytes_response[all_bytes_count - headers_bytes_count:])


def write_file(path, decoded_response):
    if decoded_response is not None:
        with open(path, 'w', encoding='utf-8') as t:
            t.write(decoded_response)
