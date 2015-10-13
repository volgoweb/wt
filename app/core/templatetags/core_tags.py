# -*- coding: utf-8 -*-
from django import template
from django.template.loader import get_template
from django.template.context import Context
from django.http import HttpResponse

register = template.Library()

@register.simple_tag()
def object_delete_btn():
    return '<span class="object-delete-btn btn btn-danger btn-sm">Удалить</span>'

