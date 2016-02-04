"""
Create singletons that may have been dropped
"""
import unicodedata
from string import digits
from string import ascii_uppercase

from django.core.management.base import BaseCommand
from nicebnf.models import NiceBnfLinks
import requests

from pyquery import PyQuery as pq






ROOT_URL = "https://www.evidence.nhs.uk"
INDEX_URL = "/formulary/bnf/current/alphalist/"


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
        except Exception as e:
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
            # we ignore appendices, who all begin with a
            ignored = "https://www.evidence.nhs.uk/formulary/bnf/current/a"
            title = unicodedata.normalize('NFKD', unicode(row.text)).encode('ascii', 'ignore')
            if not row.attrib["href"].startswith(ignored):
                result.append(dict(
                    title=title,
                    url="{0}{1}".format(ROOT_URL, row.attrib["href"])
                ))

    return result


def get_links():
    raw_html_pages = load_html()
    return process_html(raw_html_pages)


class Command(BaseCommand):
    def handle(self, *args, **options):
        links_and_urls = get_links()

        if not links_and_urls:
            raise ValueError("no links found")

        titles = [i["title"] for i in links_and_urls]
        unique_titles = set(titles)

        if len(titles) != len(unique_titles):
            import ipdb; ipdb.set_trace()

            duplicates = [i for i in titles if titles.count(i) > 1]
            raise ValueError("duplicate entries for a link found for %s" % duplicates)

        existing_links = NiceBnfLinks.objects.all()
        for i in existing_links:
            i.delete()

        nice_bnfs = []
        for link_and_url in links_and_urls:
            nice_bnfs.append(NiceBnfLinks(**link_and_url))

        NiceBnfLinks.objects.bulk_create(nice_bnfs)
        return
