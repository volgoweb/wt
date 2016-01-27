# -*- coding: utf-8 -*-
import logging
import os
from django.conf import settings
from haystack import indexes

from .models import WikiPage

tracer = logging.getLogger('elasticsearch.trace')
tracer.setLevel(logging.INFO)
tracer.addHandler(logging.FileHandler(os.path.join(settings.PROJECT_ROOT, os.pardir, 'logs', 'es_trace.log')))

class WikiPageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # performers = indexes.CharField(model_attr='performers')

    def get_model(self):
        return WikiPage
