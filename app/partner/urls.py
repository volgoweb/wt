# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from .views import (
    PartnersListPage,
    PartnerDetailPage,
    AddPartnerPage,
)

urlpatterns = patterns('',
    url(r'^$', login_required(PartnersListPage.as_view()), name='partners_list_page'),
    url(r'^partner/(?P<pk>\d+)/$', login_required(PartnerDetailPage.as_view()), name='partner_detail_page'),
    url(r'^partner/add/$', login_required(AddPartnerPage.as_view()), name='add_partner_page'),
)
