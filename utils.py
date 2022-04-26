from bs4 import BeautifulSoup
from os import mkdir
from network import HTTPClient


def write_image(path, bytes_response, all_bytes_count, headers_bytes_count):
    with open(path, 'wb') as f:
        f.write(bytes_response[all_bytes_count - headers_bytes_count:])


def write_file(path, decoded_response):
    if decoded_response is not None:
        with open(path, 'w', encoding='utf-8') as t:
            t.write(decoded_response)


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
            write_image(f'{time}/image/{image_name}',
                        response_img.bytes_response,
                        len(response_img.bytes_response),
                        int(response_img.headers['Content-Length']))
