import os
import datetime as dt
from html_parser import HTMLImageLinksParser
from network import HTTPClient


def write_image(path, bytes_response, all_bytes_count, headers_bytes_count):
    with open(path, 'wb') as f:
        f.write(bytes_response[all_bytes_count - headers_bytes_count:])


def write_file(path, decoded_response):
    if decoded_response is not None:
        with open(path, 'w', encoding='utf-8') as t:
            t.write(decoded_response)


def write_all_images_from_html(body, time, cmd_commands_url, http_version, user_agent):
    image_links_parser = HTMLImageLinksParser()
    image_links_parser.feed(body)

    image_links = image_links_parser.images

    if len(image_links) != 0:
        os.mkdir(os.path.join(time, "image"))

    for img_url in image_links:
        img_url = img_url if img_url.startswith('http') else cmd_commands_url + img_url

        try:
            response_img = HTTPClient.http_request(
                img_url,
                'GET',
                http_version,
                None,
                None,
                user_agent
            )
        except ValueError:
            print(f'Не удалось отправить запрос\nДанные:\n{img_url = }\nhttp_method = GET\n{http_version = }')
            return None
        except OSError:
            print('Не удалось отправить запрос, проблема с сокетом, попробуйте отправить запрос снова')
            return None

        image_name = img_url.split('/')[-1]

        if "Content-Type" not in response_img.headers.keys():
            return None

        content_type_img = response_img.headers["Content-Type"].replace(";", "/").split("/")[0]

        if content_type_img == 'image':
            write_image(os.path.join(time, "image", image_name),
                        response_img.bytes_response,
                        len(response_img.bytes_response),
                        int(response_img.headers['Content-Length']))


def write_http_response(url, http_method, http_version, headers, send_dt, user_agent):
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
        print(f'Не удалось отправить запрос\nДанные:\n{url = }\n{http_method = }\n{http_version = }')
        return None
    except OSError:
        print('Не удалось отправить запрос, проблема с сокетом, попробуйте отправить запрос снова')
        return None

    if "Content-Type" in response.headers.keys():
        content_type = response.headers['Content-Type'].replace(';', '/').split('/')
    else:
        content_type = None

    time = dt.datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")

    os.mkdir(time)

    if content_type is not None and content_type[0] == 'text':
        write_file(os.path.join(time, "headers.txt"), response.inf + '\n' + str(response.headers))

        if http_method != "HEAD":
            write_file(os.path.join(time, f"result.{content_type[1]}"), response.body)

        if http_method == 'GET' and content_type[1] == 'html':
            write_all_images_from_html(response.body, time, url, http_version, user_agent)

    elif content_type is not None and content_type[0] == 'image':
        write_file(os.path.join(time, "headers.txt"), response.inf + '\n' + str(response.headers))

        image_name = url.split('/')[-1]

        write_image(f'{time}/{image_name}',
                    response.bytes_response,
                    len(response.bytes_response),
                    int(response.headers['Content-Length']))
    else:
        write_file(os.path.join(time, "result.txt"), response.decoded_response)
