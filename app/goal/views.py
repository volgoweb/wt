# -*- coding: utf-8 -*-
from django.views.generic import ListView, UpdateView, CreateView
from django.db.models import Q
from django.forms.models import modelformset_factory
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponse, HttpResponseRedirect
from endless_pagination.views import AjaxListView
from endless_pagination import settings as endless_settings
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS, FieldError
from django.core.urlresolvers import reverse_lazy

from .models import Goal
from .signals import goal_saved
from .forms import GoalForm
from app.task.models import Task


class GoalsListPage(AjaxListView):
    model = Goal
    template_name = 'goal/goals_list_page.html'
    context_object_name = 'goals'
    # TODO создать кастомый queryset
    # queryset = Goal.objects.filter(deleted=False)
    # filters_form_class = GoalsListFilters

    # def __init__(self, *args, **kwargs):
    #     super(GoalsListPage, self).__init__(*args, **kwargs)
    #     self.default_filters = {
    #         'needle': '',
    #     }

    # def define_filters(self):
    #     data = {}
    #     for key, default_value in self.default_filters.items():
    #         if key in self.request.GET:
    #             data[key] = self.request.GET.get(key)
    #         else:
    #             data[key] = default_value

    #     self.filters_form = self.filters_form_class(data)
    #     self.filters_values = {}
    #     if self.filters_form.is_valid():
    #         for key in self.default_filters.keys():
    #             self.filters_values[key] = self.filters_form.cleaned_data.get(key)

    def get_base_queryset(self):
        return Goal.objects.filter(deleted=False).order_by('date_from')

    def get_queryset(self):
        qs = self.get_base_queryset()
        # if len(self.request.GET) > 0:
        # self.define_filters()

        # filter_needle = self.filters_values.get('needle')
        # if filter_needle:
        #     qs = qs.filter(
        #         Q(full_name__icontains=filter_needle) |
        #         Q(desc__icontains=filter_needle) |
        #         Q(phone__icontains=filter_needle) |
        #         Q(mobile_phone__icontains=filter_needle)
        #     )

        self.queryset = qs
        return qs

    def get_context_data(self, **kwargs):
        # TODO брать из урла и переделать модуль endless_pagination, чтобы он использовал кол-во страниц из адреса или переменной вьюса.
        self.per_page = endless_settings.PER_PAGE

        context = super(GoalsListPage, self).get_context_data(**kwargs)
        # self.define_filters()

        # фильтры списка
        # context['filters_form'] = self.filters_form

        # context['count_objects'] = self.queryset.count()
        from django.template import RequestContext
        return RequestContext(self.request, context)

    def get_page_template(self, *args, **kwargs):
        return 'goal/goals_list.html'


class CompanyGoalsListPage(GoalsListPage):
    def get_base_queryset(self):
        return Goal.objects.all().not_overdue().not_deleted().filter(performers__isnull=True).order_by('date_from')

    def get_context_data(self, **kwargs):
        context = super(GoalsListPage, self).get_context_data(**kwargs)
        context.update({
            'page_title': u'Цели компании',
        })
        return context


class DepartmentGoalsListPage(GoalsListPage):
    def get_base_queryset(self):
        return Goal.objects.all().not_overdue().not_deleted().filter(performers=self.request.user.department).order_by('date_from')

    def get_context_data(self, **kwargs):
        context = super(GoalsListPage, self).get_context_data(**kwargs)
        context.update({
            'page_title': u'Цели отдела',
        })
        return context


class MyGoalsListPage(GoalsListPage):
    def get_base_queryset(self):
        return Goal.objects.all().not_overdue().not_deleted().filter(performers=self.request.user.job).order_by('date_from')

    def get_context_data(self, **kwargs):
        context = super(GoalsListPage, self).get_context_data(**kwargs)
        context.update({
            'page_title': u'Мои цели',
        })
        return context


class GoalDetailPage(UpdateView):
    model = Goal
    form_class = GoalForm
    template_name = 'goal/goal_form_page.html'
    success_url = '/goals/my-goals/'

    def get_form_kwargs(self):
        kwargs = super(GoalDetailPage, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def get_goal_tasks(self):
        goal = self.get_object()
        tasks = Task.objects.all().not_deleted().for_goal(goal)
        return tasks

    def get_context_data(self, *args, **kwargs):
        context = super(GoalDetailPage, self).get_context_data(*args, **kwargs)
        context.update({
            'tasks': self.get_goal_tasks(),
            'show_performer': True,
            'show_author': True,
            'show_due_date': True,
        })
        return context

    def form_valid(self, form, *args, **kwargs):
        result = super(AddGoalPage, self).form_valid(form, *args, **kwargs)
        goal = self.get_object()
        goal_saved.send(sender=Goal, goal=goal, created=False, request=self.request)
        return result


class AddGoalPage(CreateView):
    model = Goal
    template_name = 'goal/goal_form_page.html'
    form_class = GoalForm
    # success_url = '/goals/my-goals/'

    def get_form_kwargs(self):
        kwargs = super(AddGoalPage, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def form_valid(self, form, *args, **kwargs):
        goal = form.save()
        goal_saved.send(sender=Goal, goal=goal, created=True, request=self.request)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('goal:my_goals_list_page')
