# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = patterns('',
    # url(r'^?(?P<list>{0})?/$'.format('|'.join(TasksList.LIST_NAMES)), login_required(TasksList.as_view()), name='tasks_list'),
    url(r'^task/(?P<pk>\d+)/$', login_required(TaskDetail.as_view()), name='task_detail'),
    url(r'^task/add/$', login_required(AddTask.as_view()), name='add_task'),
)
