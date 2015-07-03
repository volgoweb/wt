# -*- coding: utf-8 -*-
from django import template
from django.core.urlresolvers import reverse

register = template.Library()
@register.inclusion_tag('account/auth_menu.html', takes_context = True)
def auth_menu(context):
    request = context.get('request', None)
    if request:
        items = []
        auth_status = request.user.is_authenticated()
        if auth_status:
            items.append({
                'url': reverse('account:edit_profile'),
                'title': u'Редактировать профиль',
            })
            items.append({
                'url': reverse('account:logout'),
                'title': u'Выйти',
            })
        else:
            items.append({
                'url': reverse('account:login'),
                'title': u'Войти',
            })

        return {
            'items': items,
        }

