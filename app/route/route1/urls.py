# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = patterns('',
    # url(r'^$', StartRoute.as_view(), name='route1'),
    url(r'^test/$', 'app.route.route1.views.test', name='test'),
    url(r'^start-route/$', login_required(StartRoute.as_view()), name='start_route'),
)

