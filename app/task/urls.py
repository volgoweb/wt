# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = patterns('',
    # url(r'^?(?P<list>{0})?/$'.format('|'.join(TasksList.LIST_NAMES)), login_required(TasksList.as_view()), name='tasks_list'),
    url(r'^today/$', login_required(TodayTasksPage.as_view()), name='today_tasks_page'),
    # url(r'^favorite/$', login_required(FavoriteTasksPage.as_view()), name='favorite_tasks_page'),
    url(r'^overdue/$', login_required(OverdueTasksPage.as_view()), name='overdue_tasks_page'),
    url(r'^later/$', login_required(LaterTasksPage.as_view()), name='later_tasks_page'),
    url(r'^completed/$', login_required(CompletedTasksPage.as_view()), name='completed_tasks_page'),
    url(r'^outbound/$', login_required(OutboundTasksPage.as_view()), name='outbound_tasks_page'),

    url(r'^task/(?P<pk>\d+)/$', login_required(TaskDetail.as_view()), name='task_detail'),
    url(r'^task/add/$', login_required(AddTask.as_view()), name='add_task'),
)
