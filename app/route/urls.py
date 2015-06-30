# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from .route1 import urls as route1_urls
from .views import (
    ChangeTextAuthorAction,
)

urlpatterns = patterns('',
    url(r'^route1/', include(route1_urls, namespace='route1')),
    url(r'^change-text-author-action/$', login_required(ChangeTextAuthorAction.as_view()), name='change_text_author_action'),
)
