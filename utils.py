import os
import datetime as dt
from io import StringIO
from html_parser import HTMLImageLinksParser
from network import HTTPClient


def write_image(path, bytes_image_response):
    with open(path, 'wb') as f:
        f.write(bytes_image_response)


def write_file(path, decoded_response):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(decoded_response)


def get_img_response(bytes_response, headers):
    all_bytes_length = len(bytes_response)
    content_bytes_length = int(headers['Content-Length'])

    img_response_start_index = all_bytes_length - content_bytes_length

    return bytes_response[img_response_start_index:]


def write_all_images_from_html(body, time, cmd_commands_url,
                               http_version, user_agent):
    image_links_parser = HTMLImageLinksParser()
    image_links_parser.feed(body)

    image_links = image_links_parser.images

    if len(image_links) != 0:
        os.mkdir(os.path.join(time, "image"))

    for img_url in image_links:
        if not img_url.startswith('http'):
            img_url = cmd_commands_url + img_url

        response_img = HTTPClient.http_request_with_errors_handling(img_url,
                                                                    'GET',
                                                                    http_version,
                                                                    None,
                                                                    None,
                                                                    user_agent)

        image_name = img_url.split('/')[-1]

        if response_img is None \
                or "Content-Type" not in response_img.headers.keys()\
                or "Content-Length" not in response_img.headers.keys():
            continue

        content_type_header = response_img.headers["Content-Type"]
        content_type_img = content_type_header.replace(";", "/").split("/")[0]

        if content_type_img == 'image':
            img_response = get_img_response(response_img.bytes_response,
                                            response_img.headers)
            write_image(os.path.join(time, "image", image_name), img_response)


def write_http_response(url, http_method, http_version, headers,
                        send_dt, user_agent):
    response = HTTPClient.http_request_with_errors_handling(url,
                                                            http_method,
                                                            http_version,
                                                            headers,
                                                            send_dt,
                                                            user_agent)

    if response is not None and "Content-Type" in response.headers.keys():
        content_type_header = response.headers['Content-Type']
        content_type = content_type_header.replace(';', '/').split('/')
    else:
        content_type = None

    time = dt.datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")

    os.mkdir(time)

    if content_type is not None and content_type[0] == 'text':
        decoded_response = response.inf + '\n' + str(response.headers)

        if decoded_response is not None:
            write_file(os.path.join(time, "headers.txt"), decoded_response)

        if http_method != "HEAD" and response.body is not None:
            write_file(os.path.join(time, f"result.{content_type[1]}"),
                       response.body)

        if http_method == 'GET' and content_type[1] == 'html':
            write_all_images_from_html(response.body,
                                       time,
                                       url,
                                       http_version,
                                       user_agent)
    elif content_type is not None and content_type[0] == 'image':
        decoded_response = response.inf + '\n' + str(response.headers)

        if decoded_response is not None:
            write_file(os.path.join(time, "headers.txt"), decoded_response)

        image_name = url.split('/')[-1]

        if "Content-Length" not in response.headers.keys():
            return None

        img_response = get_img_response(response.bytes_response, response.headers)
        write_image(f'{time}/{image_name}', img_response)
    elif response.decoded_response is not None:
        write_file(os.path.join(time, "result.txt"),
                   response.decoded_response)
