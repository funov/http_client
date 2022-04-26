from bs4 import BeautifulSoup
import datetime as dt
from os import mkdir
from network import HTTPClient
import utils


def main():
    parser = utils.create_parser()
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

    time = str(dt.datetime.now()).replace(' ', '_').replace(':', '_').replace('-', '_').replace('.', '_')

    mkdir(time)

    if content_type is not None and content_type[0] == 'text':
        utils.write_file(f'{time}/headers.txt', response.inf + '\n' + str(response.headers))

        if cmd_commands.http_method != "HEAD":
            utils.write_file(f'{time}/result.{content_type[1]}', response.body)

        if cmd_commands.http_method == 'GET' and content_type[1] == 'html':
            write_all_images_from_html(response.body, time, cmd_commands.url, cmd_commands.http_version)

    elif content_type is not None and content_type[0] == 'image':
        utils.write_file(f'{time}/headers.txt', response.inf + '\n' + str(response.headers))

        image_name = cmd_commands.url.split('/')[-1]

        utils.write_image(f'{time}/{image_name}',
                          response.bytes_response,
                          len(response.bytes_response),
                          int(response.headers['Content-Length']))
    else:
        utils.write_file(f'{time}/result.txt', response.decoded_response)


def write_all_images_from_html(body, time, cmd_commands_url, http_version):
    soup = BeautifulSoup(body, 'html.parser')

    if len(soup.find_all('img')) != 0:
        mkdir(f'{time}/image')

    for img in soup.find_all('img'):
        url = img['src']
        url = url if url.startswith('http') else cmd_commands_url + url

        response_img = HTTPClient.http_request(
            url,
            'GET',
            http_version,
            None,
            None
        )

        image_name = url.split('/')[-1]

        if "Content-Type" not in response_img.headers.keys():
            return None

        content_type_img = response_img.headers["Content-Type"].replace(";", "/").split("/")[0]

        if content_type_img == 'image':
            utils.write_image(f'{time}/image/{image_name}',
                              response_img.bytes_response,
                              len(response_img.bytes_response),
                              int(response_img.headers['Content-Length']))


if __name__ == '__main__':
    main()
