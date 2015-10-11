# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from .views import *


urlpatterns = patterns('',
    url(r'^$', login_required(NotificationsListPage.as_view()), name='notifications_list_page'),
    url(r'^get-count.json/$', login_required(CountNotifications.as_view()), name='count_notifications'),
    url(r'^set-readed/(?P<pk>\d+)/$', 'app.notification.views.set_readed', name='set_readed'),
)
