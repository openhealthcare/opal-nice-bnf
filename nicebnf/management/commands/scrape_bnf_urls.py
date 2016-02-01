"""
Create singletons that may have been dropped
"""

from django.core.management.base import BaseCommand
from nicebnf.models import NiceBnfLinks
from nicebnf.management.commands import url_loader


class Command(BaseCommand):
    def handle(self, *args, **options):
        link_and_urls = url_loader.get_links()
        for link_and_url in link_and_urls:
            NiceBnfLinks.objects.create(**link_and_url)
        return
