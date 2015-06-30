# -*- coding: utf-8 -*-
from django import template
from django.template.loader import get_template
from django.template.context import Context
from django.http import HttpResponse

register = template.Library()

@register.inclusion_tag('route/step_actions_block.html')
def route_step_actions(step, request):
    """
    Выводит список кнопок с различными действиями, возможными на этом шаге.
    """
    actions = []
    if step:
        actions = step.get_actions(request=request)
    return {
        'step': step,
        'actions': actions,
        'request': request,
    }


