# -*- coding: utf-8 -*-
from django.views.generic import ListView, UpdateView, CreateView
from django.forms.models import modelformset_factory
from django.http import Http404
from endless_pagination.views import AjaxListView
from endless_pagination import settings as endless_settings
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS, FieldError

from .models import Task
from .forms import TasksListFilters
from app.task import forms as task_forms


class TasksList(AjaxListView):
    model = Task
    template_name = 'task/all_tasks_list_page.html'
    context_object_name = 'tasks'
    # TODO создать кастомый queryset
    # queryset = Task.objects.filter(deleted=False)
    filters_form_class = TasksListFilters
    LIST_MY_TODAY = 'my-today'
    LIST_MY_OVERDUE = 'my-overdue'
    LIST_MY_NO_DATE = 'my-no-date'
    LIST_MY_FUTURE = 'my-future'
    LIST_NAMES = [
        LIST_MY_TODAY,
        LIST_MY_OVERDUE,
        LIST_MY_NO_DATE,
        LIST_MY_FUTURE,
    ]

    @csrf_exempt
    def get(self, *args, **kwargs):
        self.default_filters = {
            'performer': self.request.user.pk,
            'project': '',
            'status': Task.STATUS_IN_WORK,
        }
        self.list_name = kwargs['list']
        return super(AllTasksList, self).get(*args, **kwargs)

    def define_filters(self):
        data = {}
        for key, default_value in self.default_filters.items():
            if key in self.request.GET:
                data[key] = self.request.GET.get(key)
            else:
                data[key] = default_value

        self.filters_form = self.filters_form_class(data)
        self.filters_values = {}
        if self.filters_form.is_valid():
            for key in self.default_filters.keys():
                self.filters_values[key] = self.filters_form.cleaned_data.get(key)

    def get_queryset(self):
        qs = Task.objects.all()
        # if len(self.request.GET) > 0:
        self.define_filters()

        filter_performer = self.filters_values.get('performer')
        if filter_performer:
            qs = qs.filter(performer=filter_performer)

        filter_project = self.filters_values.get('project')
        if filter_project:
            # TODO заменить методами кастомного queryset
            qs = qs.filter(inforeason__project=filter_project)

        filter_status = self.filters_values.get('status')
        if filter_status:
            qs = qs.filter(status=filter_status)
        self.queryset = qs
        return qs

    def get_context_data(self, **kwargs):
        # TODO брать из урла и переделать модуль endless_pagination, чтобы он использовал кол-во страниц из адреса или переменной вьюса.
        self.per_page = endless_settings.PER_PAGE

        context = super(AllTasksList, self).get_context_data(**kwargs)
        self.define_filters()

        # фильтры списка
        context['filters_form'] = self.filters_form

        context['count_objects'] = self.queryset.count()
        return context


class TaskDetail(UpdateView):
    model = Task
    # form_class = TaskForm
    template_name = 'task/task_detail.html'
    success_url = '/tasks/'

    def get_object(self, *args, **kwargs):
        obj = super(TaskDetail, self).get_object(*args, **kwargs)
        if obj.deleted:
            raise Http404(u'Эта задача удалена!')
        return obj

    def get_template_names(self):
        object_type = type(self.object)
        return 'task/task_detail/{0}.html'.format(object_type.__name__)

    def get_form_class(self):
        """
        Returns the form class to use in this view
        """
        object_type = type(self.object)
        form_class_name = '{0}Form'.format(object_type.__name__)
        return getattr(task_forms, form_class_name)

    def get_form_kwargs(self):
        kwargs = super(TaskDetail, self).get_form_kwargs()
        obj = self.get_object()
        if obj.status  == Task.STATUS_IN_WORK and obj.performer == self.request.user:
            self.can_edit = True
        else:
            self.can_edit = False
        kwargs.update({
            'request': self.request,
            'can_edit': self.can_edit,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(TaskDetail, self).get_context_data(**kwargs)
        obj = self.get_object()
        # values = self.get_task_results()

        context.update({
            'task': self.get_object(),
            'can_edit': self.can_edit,
            'task_results': obj.get_results(),
        })
        return context

    def get_success_url(self):
        obj = self.get_object()
        return '/tasks/task/{0}'.format(obj.pk)


class AddTask(CreateView):
    model = Task
    template_name = 'task/add_task.html'
    form_class = task_forms.AddTaskForm

    def get_form_kwargs(self):
        kwargs = super(AddTask, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs
