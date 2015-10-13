# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    help = "Full cache clear."

    def handle(self, *args, **options):
        cache.clear()
        print 'All caches has been cleared.'
