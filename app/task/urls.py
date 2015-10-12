# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = patterns('',
    # url(r'^?(?P<list>{0})?/$'.format('|'.join(TasksList.LIST_NAMES)), login_required(TasksList.as_view()), name='tasks_list'),
    url(r'^$', login_required(TodayTasksPage.as_view()), name='main_page'),
    url(r'^today/$', login_required(TodayTasksPage.as_view()), name='today_tasks_page'),
    url(r'^tomorrow/$', login_required(TomorrowTasksPage.as_view()), name='tomorrow_tasks_page'),
    # url(r'^favorite/$', login_required(FavoriteTasksPage.as_view()), name='favorite_tasks_page'),
    url(r'^overdue/$', login_required(OverdueTasksPage.as_view()), name='overdue_tasks_page'),
    url(r'^later/$', login_required(LaterTasksPage.as_view()), name='later_tasks_page'),
    url(r'^completed/$', login_required(CompletedTasksPage.as_view()), name='completed_tasks_page'),
    url(r'^outbound/$', login_required(OutboundTasksPage.as_view()), name='outbound_tasks_page'),
    url(r'^inbound/$', login_required(InboundTasksPage.as_view()), name='inbound_tasks_page'),
    url(r'^repeating/$', login_required(RepeatingTasksPage.as_view()), name='repeating_tasks_page'),
    url(r'^all/$', login_required(AllTasksPage.as_view()), name='all_tasks_page'),
    url(r'^get-count-tasks.json/$', login_required(CountTasks.as_view()), name='get_count_tasks'),
    url(r'^set-task-status/$', login_required(SetTaskStatus.as_view()), name='set_task_status'),

    url(r'^task/(?P<pk>\d+)/$', login_required(TaskDetail.as_view()), name='task_detail'),
    # url(r'^task/(?P<pk>\d+)/delete/$', login_required(TaskDelete.as_view()), name='task_delete'),
    url(r'^task/add/$', login_required(TaskAddForm.as_view()), name='add_task'),
)
