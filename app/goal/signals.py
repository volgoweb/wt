# -*- coding: utf-8 -*-
from django.dispatch import Signal

goal_saved = Signal(providing_args=["goal", "created", "request"])

