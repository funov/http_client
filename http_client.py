import argparse
import utils


def create_parser():
    description = "http-client, реализовано GET, POST, HEAD, PUT, " \
                  "по GET запросу получает html и картинки"

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('url', help='URL для HTTP запроса', type=str)
    parser.add_argument('http_method',
                        help='Метод HTTP запроса (GET, POST, HEAD или PUT)',
                        type=str)
    parser.add_argument('--http_version',
                        '-v',
                        help='Версия HTTP протокола (1.0 или 1.1), '
                             'если не указать будет использована 1.1',
                        type=float,
                        choices=[1.0, 1.1],
                        default=1.1)
    parser.add_argument('--headers',
                        '-he',
                        help='Заголовки для HTTP запроса в формате: '
                             '"Host: developer.mozilla.org, '
                             'Accept-Language: fr". '
                             'Если не указать будут использованы стандартные: '
                             'Host: {будет взят из URL}; '
                             'User-Agent: Mozilla/5.0 '
                             '(Windows NT 6.1; Win64; x64; rv:47.0) '
                             'Gecko/20100101 Firefox/47.0; Connection: close',
                        type=str,
                        default=None)
    parser.add_argument('--send_dt',
                        '-d',
                        help='Данные для отправки по HTTP, только для POST '
                             'или PUT, отправлять в формате "data"',
                        type=str,
                        default=None)
    parser.add_argument('--user_agent',
                        '-ua',
                        help='Выберите браузер, user-agent которого будет '
                             'использоваться в запросах, если вы указали в '
                             'headers user-agent и еще выбрали тут браузер, '
                             'приоритет будет отдан headers',
                        type=str,
                        choices=['Chrome', 'Firefox', 'Edge', 'Opera'],
                        default=None)

    return parser


def main():
    parser = create_parser()
    cmd_commands = parser.parse_args()

    try:
        utils.write_http_response(
            cmd_commands.url,
            cmd_commands.http_method,
            cmd_commands.http_version,
            cmd_commands.headers,
            cmd_commands.send_dt,
            cmd_commands.user_agent)
    except RuntimeError:
        print('Что-то пошло не так, напишите разработчикам')


if __name__ == '__main__':
    main()
