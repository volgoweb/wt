# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from .views import (
    ClientsListPage,
    ClientDetailPage,
    AddClientPage,
)

urlpatterns = patterns('',
    url(r'^$', login_required(ClientsListPage.as_view()), name='clients_list_page'),
    url(r'^client/(?P<pk>\d+)/$', login_required(ClientDetailPage.as_view()), name='client_detail_page'),
    url(r'^client/add/$', login_required(AddClientPage.as_view()), name='add_client_page'),
)
