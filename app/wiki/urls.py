# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = patterns('',
    url(r'^$', WikiList.as_view(), name='wiki_list_page'),
    #url(r'^(?P<slug>[^/]+)/$', 'main.portfolio.views.portfolio_detail_page', name='portfolio__portfolio_detail_page'),
    url(r'^wiki-page/(?P<pk>\d+)/$', login_required(WikiPageDetail.as_view()), name='wiki_page_detail'),
    url(r'^wiki-page-block/(?P<pk>\d+)/$', login_required(WikiPageBlockDetail.as_view()), name='wiki_page_detail_block'),
    url(r'^add-wiki-page/$', login_required(AddWikiPage.as_view()), name='add_wiki_page'),
)
