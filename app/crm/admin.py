# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import DealStatus

class DealStatusAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title']

admin.site.register(DealStatus, DealStatusAdmin);
