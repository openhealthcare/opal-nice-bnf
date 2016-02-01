import requests

from pyquery import PyQuery as pq
from string import digits
from string import ascii_uppercase

ROOT_URL = "https://www.evidence.nhs.uk/"
INDEX_URL = "formulary/bnf/current/alphalist/"


def load_html():
    all_indexes = []
    for i in [digits, ascii_uppercase]:
        all_indexes.extend(i)
    urls = ["{0}{1}{2}".format(ROOT_URL, INDEX_URL, i) for i in all_indexes]

    raw_html_pages = []

    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code > 399:
                print "failed to get {0} with {1}".format(
                    url, response.status_code
                )
            else:
                raw_html_pages.append(response.text)
        except e:
            print "failed to get {}".format(url)
            print e

    if not len(urls):
        raise "unable to get any urls"

    return raw_html_pages


def process_html(raw_html_pages):
    result = []
    for raw_html_page in raw_html_pages:
        parsed = pq(raw_html_page)
        for row in parsed(".media-body .media-title a"):
            result.append(dict(
                title=row.text,
                url="{0}{1}".format(ROOT_URL, row.attrib["href"])
            ))

    return result


def get_links():
    raw_html_pages = load_html()
    return process_html(raw_html_pages)
