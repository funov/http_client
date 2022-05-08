import os
import datetime as dt
from io import StringIO
from html_parser import HTMLImageLinksParser
from network import HTTPClient


def write_image(path, bytes_response, all_bytes_count, headers_bytes_count):
    with open(path, 'wb') as f:
        f.write(bytes_response[all_bytes_count - headers_bytes_count:])


def write_file(path, decoded_response):
    if decoded_response is not None:
        with open(path, 'w', encoding='utf-8') as t:
            t.write(decoded_response)


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

        response_img = send_request_with_errors_handling(img_url,
                                                         'GET',
                                                         http_version,
                                                         None,
                                                         None,
                                                         user_agent)

        image_name = img_url.split('/')[-1]

        if response_img is None \
                or "Content-Type" not in response_img.headers.keys():
            continue

        content_type_header = response_img.headers["Content-Type"]
        content_type_img = content_type_header.replace(";", "/").split("/")[0]

        if content_type_img == 'image':
            write_image(os.path.join(time, "image", image_name),
                        response_img.bytes_response,
                        len(response_img.bytes_response),
                        int(response_img.headers['Content-Length']))


def write_http_response(url, http_method, http_version, headers,
                        send_dt, user_agent):
    response = send_request_with_errors_handling(url,
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
        write_file(os.path.join(time, "headers.txt"),
                   response.inf + '\n' + str(response.headers))

        if http_method != "HEAD":
            write_file(os.path.join(time, f"result.{content_type[1]}"),
                       response.body)

        if http_method == 'GET' and content_type[1] == 'html':
            write_all_images_from_html(response.body,
                                       time,
                                       url,
                                       http_version,
                                       user_agent)

    elif content_type is not None and content_type[0] == 'image':
        write_file(os.path.join(time, "headers.txt"),
                   response.inf + '\n' + str(response.headers))

        image_name = url.split('/')[-1]

        write_image(f'{time}/{image_name}',
                    response.bytes_response,
                    len(response.bytes_response),
                    int(response.headers['Content-Length']))
    else:
        write_file(os.path.join(time, "result.txt"),
                   response.decoded_response)


def send_request_with_errors_handling(url, http_method, http_version,
                                      headers, send_dt, user_agent):
    try:
        response = HTTPClient.http_request(
            url,
            http_method,
            http_version,
            headers,
            send_dt,
            user_agent
        )
    except ValueError:
        print(f'Не удалось отправить запрос\nДанные:'
              f'\n{url = }\n{http_method = }\n{http_version = }')
        return None
    except OSError:
        print('Не удалось отправить запрос, проблема с сокетом, '
              'попробуйте отправить запрос снова')
        return None

    if response.inf.split()[1][0] == '3' \
            and 'Location' in response.headers.keys():
        url = response.headers['Location']

        print(f"Перенаправлено на {url}")

        response = send_request_with_errors_handling(url,
                                                     http_method,
                                                     http_version,
                                                     headers,
                                                     send_dt,
                                                     user_agent)

    return response
