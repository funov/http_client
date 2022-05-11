import os
import html_parser
import datetime as dt
from network import HTTPClient


def write_file(path, decoded_response):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(decoded_response)


def write_image(path, bytes_image_response):
    with open(path, 'wb') as f:
        f.write(bytes_image_response)


def write_all_images(folder_name, image_name_to_image_bytes):
    for image_name in image_name_to_image_bytes.keys():
        write_image(
            os.path.join(folder_name, "image", image_name),
            image_name_to_image_bytes[image_name])


def get_image_bytes(bytes_response, headers):
    all_bytes_length = len(bytes_response)
    content_bytes_length = int(headers['Content-Length'])

    img_response_start_index = all_bytes_length - content_bytes_length

    return bytes_response[img_response_start_index:]


def get_all_images_bytes(image_links, base_url, http_version, user_agent):
    image_name_to_image_bytes = {}

    for img_url in image_links:
        if not img_url.startswith('http'):
            img_url = base_url + '/' + img_url

        response_img = HTTPClient.http_request_with_errors_handling(
            img_url,
            'GET',
            http_version,
            None,
            None,
            user_agent)

        image_name = img_url.split('/')[-1]

        if response_img is None \
                or "Content-Type" not in response_img.headers_dict.keys()\
                or "Content-Length" not in response_img.headers_dict.keys():
            continue

        content_type_header = response_img.headers_dict["Content-Type"]
        content_type_img = content_type_header.replace(";", "/").split("/")[0]

        if content_type_img == 'image':
            image_bytes = get_image_bytes(
                response_img.bytes_response,
                response_img.headers_dict)

            image_name_to_image_bytes[image_name] = image_bytes

    return image_name_to_image_bytes


def write_html_with_images_response(
        folder_name, response, http_method,
        content_type, url, http_version, user_agent):
    write_file(os.path.join(folder_name, "headers.txt"), response.head)

    if http_method != "HEAD" and response.body is not None:
        write_file(
            os.path.join(folder_name, f"result.{content_type[1]}"),
            response.body)

    if http_method == 'GET' and content_type[1] == 'html':
        image_links = html_parser.get_image_links_from_html(response.body)
        image_name_to_image_bytes = get_all_images_bytes(
            image_links,
            url,
            http_version,
            user_agent)

        if len(image_name_to_image_bytes.keys()) != 0:
            os.mkdir(os.path.join(folder_name, "image"))
            write_all_images(folder_name, image_name_to_image_bytes)


def write_one_image_response(folder_name, response, url):
    write_file(os.path.join(folder_name, "headers.txt"), response.head)

    image_name = url.split('/')[-1]

    if "Content-Length" not in response.headers_dict.keys():
        return None

    img_bytes = get_image_bytes(
        response.bytes_response,
        response.headers_dict)

    write_image(os.path.join(folder_name, image_name), img_bytes)


def write_http_response(url, http_method, http_version, headers,
                        send_dt, user_agent):
    response = HTTPClient.http_request_with_errors_handling(
        url,
        http_method,
        http_version,
        headers,
        send_dt,
        user_agent)

    if response is not None \
            and "Content-Type" in response.headers_dict.keys():
        content_type_header = response.headers_dict['Content-Type']
        content_type = content_type_header.replace(';', '/').split('/')
    else:
        content_type = None

    time = dt.datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")

    os.mkdir(time)

    if content_type is not None and content_type[0] == 'text':
        write_html_with_images_response(
            time, response, http_method, content_type,
            url, http_version, user_agent)
    elif content_type is not None and content_type[0] == 'image':
        write_one_image_response(time, response, url)
    elif response.decoded_response is not None:
        write_file(
            os.path.join(time, "result.txt"),
            response.decoded_response)
