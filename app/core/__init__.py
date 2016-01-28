# -*- coding: utf-8 -*-
import logging
from django.conf import settings


tracer = logging.getLogger('elasticsearch.trace')
tracer.setLevel(logging.INFO)
tracer.addHandler(logging.FileHandler(settings.ELASTICSEARCH_LOG))