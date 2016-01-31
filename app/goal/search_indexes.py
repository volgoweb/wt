# -*- coding: utf-8 -*-
import logging
import os
from django.conf import settings
from haystack import indexes

from .models import Goal


class WikiPageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # performers = indexes.CharField(model_attr='performers')

    def get_model(self):
        return Goal