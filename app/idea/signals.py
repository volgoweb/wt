# -*- coding: utf-8 -*-
from django.dispatch import Signal

idea_saved = Signal(providing_args=["idea", "created", "request"])

