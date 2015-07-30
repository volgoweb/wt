# -*- coding: utf-8 -*-
from django.views.generic import ListView, UpdateView, CreateView
from django.forms.models import modelformset_factory
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponse
from endless_pagination.views import AjaxListView
from endless_pagination import settings as endless_settings
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS, FieldError
from django.core.urlresolvers import reverse_lazy

from .models import Task, TaskFile, TaskTemplate
from .forms import TasksListFilters, TaskFileForm
from app.task import forms as task_forms
from app.core.models import FileItem
from app.core.forms import FileItemForm


FilesFormset = generic_inlineformset_factory(
    FileItem,
    form=FileItemForm,
    ct_field='owner_type',
    fk_field='owner_id',
    fields=['file'],
    extra=0,
)


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

    # @csrf_exempt
    # def get(self, *args, **kwargs):
    #     if 'only_count' in kwargs:
    #         count = self.get_base_queryset().count()
    #         return HttpResponse(count)

    #     return super(TasksList, self).get(*args, **kwargs)

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

    @classmethod
    def get_base_queryset_from_class(cls, request):
        pass

    @classmethod
    def get_base_count_from_class(cls, request):
        qs = cls.get_base_queryset_from_class(request)
        return qs.count()

    def get_base_queryset(self):
        return self.__class__.get_base_queryset_from_class(self.request)

    def get_queryset(self):
        qs = self.get_base_queryset()
        # if len(self.request.GET) > 0:
        # self.define_filters()

        # filter_performer = self.filters_values.get('performer')
        # if filter_performer:
        #     qs = qs.filter(performer=filter_performer)

        # filter_project = self.filters_values.get('project')
        # if filter_project:
        #     # TODO заменить методами кастомного queryset
        #     qs = qs.filter(inforeason__project=filter_project)

        # filter_status = self.filters_values.get('status')
        # if filter_status:
        #     qs = qs.filter(status=filter_status)
        # self.queryset = qs
        return qs

    def get_context_data(self, **kwargs):
        # TODO брать из урла и переделать модуль endless_pagination, чтобы он использовал кол-во страниц из адреса или переменной вьюса.
        self.per_page = endless_settings.PER_PAGE

        context = super(TasksList, self).get_context_data(**kwargs)
        # self.define_filters()

        context['Task'] = Task
        context['form'] = task_forms.TaskTemplateForm(request=self.request, is_shortform=True)
        context['files_formset'] = FilesFormset()

        # фильтры списка
        # context['filters_form'] = self.filters_form

        # context['count_objects'] = self.queryset.count()
        from django.template import RequestContext
        return RequestContext(self.request, context)


# class FavoriteTasksPage(TasksList):
#     @classmethod
#     def get_base_queryset_from_class(cls, request):
#         return Task.objects.all().performed(request.user).in_work().favorite()


class TodayTasksPage(TasksList):
    @classmethod
    def get_base_queryset_from_class(cls, request):
        return Task.objects.all().performed(request.user).in_work().today()

    def get_context_data(self, **kwargs):
        context = super(TodayTasksPage, self).get_context_data(**kwargs)
        context.update({
            'page_title': u'Задачи на сегодня',
            'show_due_date': False,
        })
        return context


class OverdueTasksPage(TasksList):
    @classmethod
    def get_base_queryset_from_class(cls, request):
        return Task.objects.all().performed(request.user).in_work().today()

    def get_context_data(self, **kwargs):
        context = super(OverdueTasksPage, self).get_context_data(**kwargs)
        context.update({
            'page_title': u'Задачи просроченные',
            'show_due_date': True,
        })
        return context


class LaterTasksPage(TasksList):
    @classmethod
    def get_base_queryset_from_class(cls, request):
        return Task.objects.all().performed(request.user).in_work().later_than_today_or_without_due()

    def get_context_data(self, **kwargs):
        context = super(LaterTasksPage, self).get_context_data(**kwargs)
        context.update({
            'page_title': u'Задачи на будущее',
            'show_due_date': True,
        })
        return context


class CompletedTasksPage(TasksList):
    @classmethod
    def get_base_queryset_from_class(cls, request):
        return Task.objects.all().performed(request.user).completed()

    def get_context_data(self, **kwargs):
        context = super(CompletedTasksPage, self).get_context_data(**kwargs)
        context.update({
            'page_title': u'Задачи выполненные',
            'show_due_date': True,
        })
        return context


class OutboundTasksPage(TasksList):
    @classmethod
    def get_base_queryset_from_class(cls, request):
        return Task.objects.all().consigned(request.user, exclude_self_tasks=True).in_work()

    def get_context_data(self, **kwargs):
        context = super(OutboundTasksPage, self).get_context_data(**kwargs)
        context.update({
            'page_title': u'Задачи исходящие',
            'show_performer': True,
            'show_due_date': True,
        })
        return context


class RepeatingTasksPage(TasksList):
    @classmethod
    def get_base_queryset_from_class(cls, request):
        return Task.objects.all().consigned(request.user).repeating()

    def get_context_data(self, **kwargs):
        context = super(RepeatingTasksPage, self).get_context_data(**kwargs)
        context.update({
            'page_title': u'Задачи повторяющиеся',
            'show_performer': False,
            'show_due_date': False,
        })
        return context


class TaskDetail(UpdateView):
    model = Task
    # form_class = TaskForm
    template_name = 'task/task_detail.html'
    success_url = '/tasks/'

    def get_files_formset(self, *args, **kwargs):
        obj = self.get_object()
        qs = FileItem.objects.none()
        if getattr(obj, 'pk', None):
            task_type = ContentType.objects.get(app_label='task', model='task')
            qs = FileItem.objects.filter(owner_id=obj.pk, owner_type=task_type.pk)
        formset = FilesFormset(data=self.request.POST or None, files=self.request.FILES or None, queryset=qs, instance=obj)
        return formset

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
        if obj.status  in (Task.STATUS_IN_WORK, Task.STATUS_AWATING_EXECUTION) and obj.template.performer == self.request.user:
            self.can_edit = True
        else:
            self.can_edit = False
        kwargs.update({
            'request': self.request,
            'can_edit': self.can_edit,
        })
        return kwargs

    def get_template_form(self):
        obj = self.get_object()
        form = task_forms.TaskTemplateForm(
            data=self.request.POST or None,
            instance=obj.template,
            prefix='tpl',
            request=self.request,
            task=obj,
        )
        return form

    def get_context_data(self, **kwargs):
        context = super(TaskDetail, self).get_context_data(**kwargs)
        obj = self.get_object()
        performer = obj.template.performer
        if performer and self.request.user != obj.author:
            performer_view = True
        else:
            performer_view = False
        context.update({
            'task': self.get_object(),
            'performer_view': performer_view,
            'can_edit': self.can_edit,
            'task_results': obj.get_results(),
            'template_form': self.get_template_form(),
            'files_formset': self.get_files_formset(),
        })
        return context

    def form_valid(self, form):
        is_invalid_formset = True
        if self.request.POST.get('repeat-period') and not self.request.POST.get('due_date'):
            due_date_errors = form.errors.get('due_date', '')
            form.errors['due_date'] = due_date_errors + u' При выборе периода повторения обязательно укажите срок исполнения.'
            return self.form_invalid(form)
        template_form = self.get_template_form()
        if form.is_valid() and template_form.is_valid():
            task = form.save(commit=False)
            task_tpl = template_form.save(commit=False)
            files_formset = self.get_files_formset()
            if files_formset.is_valid():
                task = form.save(commit=True)
                task_tpl = template_form.save(commit=True)
                files_formset.save()
            else:
                is_invalid_formset = False

        if is_invalid_formset:
            return super(TaskDetail, self).form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        obj = self.get_object()
        return '/tasks/task/{0}'.format(obj.pk)


class TemplateFormMixin(object):
    model = TaskTemplate
    # template_name = 'task/add_task.html'
    template_name = 'task/template_form.html'
    form_class = task_forms.TaskTemplateForm
    # success_url = '/tasks/today/'

    def get_form_kwargs(self):
        kwargs = super(TemplateFormMixin, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def get_files_formset(self, *args, **kwargs):
        formset = FilesFormset(data=self.request.POST or None, files=self.request.FILES or None, instance=kwargs.get('instance', None))
        return formset

    def get_context_data(self, *args, **kwargs):
        context = super(TemplateFormMixin, self).get_context_data(*args, **kwargs)
        context['files_formset'] = self.get_files_formset()
        return context

    def form_valid(self, form):
        is_valid_formset = True
        task_tpl = form.save(commit=False)
        files_formset = self.get_files_formset(instance=task_tpl)
        if files_formset.is_valid():
            task_tpl = form.save(commit=True)
            files_formset.save()
        else:
            is_valid_formset = False
            # print '------------------ files_formset.is_INvalid'

        if is_valid_formset:
            return super(TemplateFormMixin, self).form_valid(form)
        else:
            return self.form_invalid(form)


class TaskAddForm(TemplateFormMixin, CreateView):
    template_name = 'task/add_task_page.html'

    def get_success_url(self, *args, **kwargs):
        return self.request.GET.get('next', '/tasks/today/')
