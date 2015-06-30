# -*- coding: utf-8 -*-
from django.dispatch import Signal

task_saved = Signal(providing_args=["task"])
