# -*- coding: utf-8 -*-
from django.db import models

from helper import models as helper_models


class FileItem(helper_models.FileItem):
    class Meta:
        abstract = False
