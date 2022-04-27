import argparse
import datetime as dt
from network import HTTPClient
import utils
import os


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


def main():
    parser = create_parser()
    cmd_commands = parser.parse_args()

    response = HTTPClient.http_request(
        cmd_commands.url,
        cmd_commands.http_method,
        cmd_commands.http_version,
        cmd_commands.headers,
        cmd_commands.send_dt
    )

    content_type = response.headers['Content-Type'].replace(';', '/').split('/') \
        if "Content-Type" in response.headers.keys() \
        else None

    time = dt.datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")

    os.mkdir(time)

    if content_type is not None and content_type[0] == 'text':
        utils.write_file(os.path.join(time, "headers.txt"), response.inf + '\n' + str(response.headers))

        if cmd_commands.http_method != "HEAD":
            utils.write_file(os.path.join(time, f"result.{content_type[1]}"), response.body)

        if cmd_commands.http_method == 'GET' and content_type[1] == 'html':
            utils.write_all_images_from_html(response.body, time, cmd_commands.url, cmd_commands.http_version)

    elif content_type is not None and content_type[0] == 'image':
        utils.write_file(os.path.join(time, "headers.txt"), response.inf + '\n' + str(response.headers))

        image_name = cmd_commands.url.split('/')[-1]

        utils.write_image(f'{time}/{image_name}',
                          response.bytes_response,
                          len(response.bytes_response),
                          int(response.headers['Content-Length']))
    else:
        utils.write_file(os.path.join(time, "result.txt"), response.decoded_response)


if __name__ == '__main__':
    main()
