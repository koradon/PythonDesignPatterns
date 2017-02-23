import httplib2
import os
import re
import threading
from urllib.parse import urlparse, urljoin
from urllib.request import urlretrieve
from bs4 import BeautifulSoup


class Singleton(object):
    downloaded = set()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


class ImageDownloaderThread(threading.Thread):
    """
    A thread for downloading images in parallel.
    """
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print("Starting threading {}".format(self.name))
        download_images(self.name)
        print("Finished thread {}".format(self.name))

def download_images(thread_name):
    singleton = Singleton()

    while singleton.to_visit:
        url = singleton.to_visit.pop()

        http = httplib2.Http()
        print("{thread} Starting downloading images from {url}"
              .format(thread=thread_name,
                      url=url))

        try:
            status, response = http.request(url)

        except Exception:
            continue

        bs = BeautifulSoup(response, 'html.parser')
        images = BeautifulSoup.findAll(bs, 'img')

        for image in images:
            src = image.get('src')
            src = urljoin(url, src)

            basename = os.path.basename(src)

            if src not in singleton.downloaded:
                singleton.downloaded.add(src)
                print('Downloading {}'.format(src))
                urlretrieve(src, os.path.join('images', basename))

        print("{thread} finished downloading images from {url}"
              .format(thread=thread_name,
                      url=url))


def traverse_site(max_links=10):
    link_parser_singleton = Singleton()

    while link_parser_singleton.queue_to_parse:
        if len(link_parser_singleton.to_visit) == max_links:
            return

        url = link_parser_singleton.queue_to_parse.pop()

        http = httplib2.Http()
        try:
            status, response = http.request(url)
        except Exception:
            continue

        # skip if not webpage
        if status.get('content-type') != 'text/html':
            continue

        # add the link to queue for downloading image
        link_parser_singleton.to_visit.add(url)
        print("Added {} to queue".format(url))

        bs = BeautifulSoup(response, "html.parser")

        for link in BeautifulSoup.findAll(bs, 'a'):
            link_url = link.get('href')

            if not link_url:
                continue

            parsed = urlparse(link_url)

            if parsed.netloc:
                continue

            link_url = (parsed.scheme or parsed.root.scheme) + \
                       "//" + \
                       (parsed.netloc or parsed.root.netloc) + \
                       parsed.path or ''

            if link_url in link_parser_singleton.to_visit:
                continue

            link_parser_singleton.queue_to_parse = \
                [link_url] + link_parser_singleton.queue_to_parse


if __name__ == '__main__':
    root = 'https://www.wikipedia.org/'

    parsed_root = urlparse(root)

    singleton = Singleton()
    singleton.queue_to_parse = [root]
    singleton.to_visit = set()
    singleton.donloaded = set()

    traverse_site()

    if not os.path.exists('images'):
        os.mkdir('images')

    thread1 = ImageDownloaderThread(1, "Thread-1", 1)
    thread2 = ImageDownloaderThread(1, "Thread-2", 2)

    thread1.start()
    thread2.start()



































