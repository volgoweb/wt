# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from .views import *
from .perm_decorators import (
    has_access_to_view_wiki_page,
    has_access_to_edit_wiki_page,
)

urlpatterns = patterns('',
    url(r'^$', WikiList.as_view(), name='wiki_list_page'),
    #url(r'^(?P<slug>[^/]+)/$', 'main.portfolio.views.portfolio_detail_page', name='portfolio__portfolio_detail_page'),
    url(r'^wiki-page/(?P<pk>\d+)/$', has_access_to_view_wiki_page(WikiPageDetail.as_view()), name='wiki_page_detail'),
    url(r'^wiki-page/(?P<pk>\d+)/edit/$', has_access_to_edit_wiki_page(EditWikiPage.as_view()), name='edit_wiki_page'),
    url(r'^wiki-page-block/(?P<pk>\d+)/$', has_access_to_view_wiki_page(WikiPageBlockDetail.as_view()), name='wiki_page_detail_block'),
    url(r'^add-wiki-page/$', login_required(AddWikiPage.as_view()), name='add_wiki_page'),
)
