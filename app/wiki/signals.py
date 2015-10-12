# -*- coding: utf-8 -*-
from django.dispatch import Signal

wiki_page_saved = Signal(providing_args=["wiki_page", "created", "request"])

