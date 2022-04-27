from html_parser import HTMLImageLinksParser
from network import HTTPClient
import os


def write_image(path, bytes_response, all_bytes_count, headers_bytes_count):
    with open(path, 'wb') as f:
        f.write(bytes_response[all_bytes_count - headers_bytes_count:])


def write_file(path, decoded_response):
    if decoded_response is not None:
        with open(path, 'w', encoding='utf-8') as t:
            t.write(decoded_response)


def write_all_images_from_html(body, time, cmd_commands_url, http_version):
    image_links_parser = HTMLImageLinksParser()
    image_links_parser.feed(body)

    image_links = image_links_parser.images

    if len(image_links) != 0:
        os.mkdir(os.path.join(time, "image"))

    for img_url in image_links:
        img_url = img_url if img_url.startswith('http') else cmd_commands_url + img_url

        response_img = HTTPClient.http_request(
            img_url,
            'GET',
            http_version,
            None,
            None
        )

        image_name = img_url.split('/')[-1]

        if "Content-Type" not in response_img.headers.keys():
            return None

        content_type_img = response_img.headers["Content-Type"].replace(";", "/").split("/")[0]

        if content_type_img == 'image':
            write_image(os.path.join(time, "image", image_name),
                        response_img.bytes_response,
                        len(response_img.bytes_response),
                        int(response_img.headers['Content-Length']))
