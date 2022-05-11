from html.parser import HTMLParser


class HTMLImageLinksParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for attr in attrs:
                if attr[0] == 'src':
                    self.images.append(attr[1])


def get_image_links_from_html(html):
    image_links_parser = HTMLImageLinksParser()
    image_links_parser.feed(html)

    return image_links_parser.images
