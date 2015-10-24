# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from .views import (
    IdeasListPage,
    IdeaDetailPage,
    IdeaEditPage,
    AddIdeaPage,
)

urlpatterns = patterns('',
    url(r'^ideas/$', login_required(IdeasListPage.as_view()), name='ideas_list_page'),
    url(r'^(?P<pk>\d+)/edit/$', login_required(IdeaEditPage.as_view()), name='idea_edit_page'),
    url(r'^(?P<pk>\d+)/$', login_required(IdeaDetailPage.as_view()), name='idea_detail_page'),
    url(r'^add-idea/$', login_required(AddIdeaPage.as_view()), name='add_idea_page'),
)

