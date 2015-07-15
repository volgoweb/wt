# -*- coding: utf-8 -*-
from functools import wraps
from django.utils.decorators import available_attrs
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from .models import WikiPage

def has_user_perm_in_wiki_page(view_func, perm):
    @wraps(view_func, assigned=available_attrs(view_func))
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        p = get_object_or_404(WikiPage, pk=kwargs.get('pk', None))
        # проверка разрешен ли пользователю доступ на просмотр
        if p.has_user_perm_in_wiki_page(request.user, perm):
            return view_func(request, *args, **kwargs)
        raise PermissionDenied

    return wrapped_view


def has_access_to_view_wiki_page(view_func):
    return has_user_perm_in_wiki_page(view_func, WikiPage.PERM_VIEW)


def has_access_to_edit_wiki_page(view_func):
    return has_user_perm_in_wiki_page(view_func, WikiPage.PERM_EDIT)
