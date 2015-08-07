# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from .views import (
    CompanyGoalsListPage,
    DepartmentGoalsListPage,
    MyGoalsListPage,
    GoalDetailPage,
    AddGoalPage,
)

urlpatterns = patterns('',
    url(r'^company-goals/$', login_required(CompanyGoalsListPage.as_view()), name='company_goals_list_page'),
    url(r'^department-goals/$', login_required(DepartmentGoalsListPage.as_view()), name='department_goals_list_page'),
    url(r'^my-goals/$', login_required(MyGoalsListPage.as_view()), name='my_goals_list_page'),
    url(r'^(?P<pk>\d+)/$', login_required(GoalDetailPage.as_view()), name='goal_detail_page'),
    url(r'^add-goal/$', login_required(AddGoalPage.as_view()), name='add_goal_page'),
)

