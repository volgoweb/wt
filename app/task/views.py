# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, UpdateView, CreateView, View
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponse
from endless_pagination.views import AjaxListView
from endless_pagination import settings as endless_settings
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS, FieldError
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages

from .models import Task, TaskFile, TaskTemplate
from .forms import TasksListFilters, TaskFileForm
from app.task import forms as task_forms
from app.core.models import FileItem
from app.core.forms import FileItemForm
from .signals import task_saved


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
    template_name = 'task/tasks_list_page.html'
    context_object_name = 'tasks'
    # TODO создать кастомый queryset
    # queryset = Task.objects.filter(deleted=False)
    filters_form_class = TasksListFilters
    LIST_MY_TODAY = 'my-today'
    LIST_MY_TOMORROW = 'my-tomorrow'
    LIST_MY_OVERDUE = 'my-overdue'
    LIST_MY_NO_DATE = 'my-no-date'
    LIST_MY_FUTURE = 'my-future'
    LIST_MY_COMPLETED = 'my-completed'
    LIST_MY_INBOUND = 'my-inbound'
    LIST_MY_OUTBOUND = 'my-outbound'
    LIST_MY_REPEATING = 'my-repeating'
    LIST_ALL = 'all'
    LIST_NAMES = [
        LIST_MY_TODAY,
        LIST_MY_TOMORROW,
        LIST_MY_OVERDUE,
        LIST_MY_NO_DATE,
        LIST_MY_FUTURE,
        LIST_MY_COMPLETED,
        LIST_MY_INBOUND,
        LIST_MY_OUTBOUND,
        LIST_MY_REPEATING,
        LIST_ALL,
    ]

    def __init__(self, *args, **kwargs):
        super(TasksList, self).__init__(*args, **kwargs)
        self.default_filters = {}

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
        if len(self.request.GET) > 0:
            self.define_filters()

            filter_search = self.filters_values.get('search')
            if filter_search:
                qs = qs.filter(
                    Q(template__title__icontains=filter_search) |
                    Q(template__desc__icontains=filter_search)
                )

            filter_performer = self.filters_values.get('performer')
            if filter_performer:
                qs = qs.filter(template__performer=filter_performer)

            filter_author = self.filters_values.get('author')
            if filter_author:
                qs = qs.filter(template__author=filter_author)

            filter_status = self.filters_values.get('status')
            if filter_status:
                qs = qs.filter(status=filter_status)
        self.queryset = qs
        return qs

    def get_page_template(self, *args, **kwargs):
        return 'task/tasks_list_block.html'

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
#         return Task.objects.all().performed(request.user).in_work_or_wait().favorite()


class TodayTasksPage(TasksList):
    @classmethod
    def get_base_queryset_from_class(cls, request):
        return Task.objects.all().performed(request.user).in_work_or_wait().today().order_by('due_date')

    def get_context_data(self, **kwargs):
        context = super(TodayTasksPage, self).get_context_data(**kwargs)
        context.update({
            'page_title': u'Задачи на сегодня',
            'list_name': self.LIST_MY_TODAY,
            'show_author': True,
            'show_due_date': True,
        })
        return context


class TomorrowTasksPage(TasksList):
    @classmethod
    def get_base_queryset_from_class(cls, request):
        return Task.objects.all().performed(request.user).in_work_or_wait().tomorrow().order_by('due_date')

    def get_context_data(self, **kwargs):
        context = super(TomorrowTasksPage, self).get_context_data(**kwargs)
        context.update({
            'page_title': u'Задачи на завтра',
            'list_name': self.LIST_MY_TOMORROW,
            'show_author': True,
            'show_due_date': True,
        })
        return context


class OverdueTasksPage(TasksList):
    @classmethod
    def get_base_queryset_from_class(cls, request):
        return Task.objects.all().performed(request.user).in_work_or_wait().overdue().order_by('due_date')

    def get_context_data(self, **kwargs):
        context = super(OverdueTasksPage, self).get_context_data(**kwargs)
        context.update({
            'page_title': u'Задачи просроченные',
            'list_name': self.LIST_MY_OVERDUE,
            'show_author': True,
            'show_due_date': True,
        })
        return context


class LaterTasksPage(TasksList):
    @classmethod
    def get_base_queryset_from_class(cls, request):
        return Task.objects.all().performed(request.user).in_work_or_wait().later_than_today_or_without_due().order_by('due_date')

    def get_context_data(self, **kwargs):
        context = super(LaterTasksPage, self).get_context_data(**kwargs)
        context.update({
            'page_title': u'Задачи на будущее',
            'list_name': self.LIST_MY_FUTURE,
            'show_author': True,
            'show_due_date': True,
        })
        return context


class CompletedTasksPage(TasksList):
    @classmethod
    def get_base_queryset_from_class(cls, request):
        return Task.objects.all().performed(request.user).completed().order_by('due_date')

    def get_context_data(self, **kwargs):
        context = super(CompletedTasksPage, self).get_context_data(**kwargs)
        context.update({
            'page_title': u'Задачи выполненные',
            'list_name': self.LIST_MY_COMPLETED,
            'show_author': True,
            'show_due_date': True,
        })
        return context


class InboundTasksPage(TasksList):
    @classmethod
    def get_base_queryset_from_class(cls, request):
        return Task.objects.all().performed(request.user, exclude_self_tasks=True).in_work_or_wait().order_by('due_date')

    def get_context_data(self, **kwargs):
        context = super(InboundTasksPage, self).get_context_data(**kwargs)
        context.update({
            'page_title': u'Задачи входящие',
            'list_name': self.LIST_MY_INBOUND,
            # 'show_performer': True,
            'show_author': True,
            'show_due_date': True,
        })
        return context


class OutboundTasksPage(TasksList):
    @classmethod
    def get_base_queryset_from_class(cls, request):
        return Task.objects.all().consigned(request.user, exclude_self_tasks=True).in_work_or_wait().order_by('due_date')

    def get_context_data(self, **kwargs):
        context = super(OutboundTasksPage, self).get_context_data(**kwargs)
        context.update({
            'page_title': u'Задачи исходящие',
            'list_name': self.LIST_MY_OUTBOUND,
            'show_performer': True,
            'show_due_date': True,
        })
        return context


class RepeatingTasksPage(TasksList):
    @classmethod
    def get_base_queryset_from_class(cls, request):
        return Task.objects.all().consigned(request.user).repeating().order_by('due_date')

    def get_context_data(self, **kwargs):
        context = super(RepeatingTasksPage, self).get_context_data(**kwargs)
        context.update({
            'page_title': u'Задачи повторяющиеся',
            'list_name': self.LIST_MY_REPEATING,
            'show_performer': False,
            'show_due_date': False,
        })
        return context


class AllTasksPage(TasksList):
    template_name = 'task/tasks_list_all_page.html'

    def __init__(self, *args, **kwargs):
        super(TasksList, self).__init__(*args, **kwargs)
        self.default_filters = {
            'search': '',
            'performer': None,
            'author': None,
            'status': None,
        }
    @classmethod
    def get_base_queryset_from_class(cls, request):
        return Task.objects.all().order_by('due_date')

    def get_page_template(self, *args, **kwargs):
        return 'task/tasks_list_all_block.html'

    def get_context_data(self, **kwargs):
        self.define_filters()
        context = super(AllTasksPage, self).get_context_data(**kwargs)
        context.update({
            'filters_form': self.filters_form,
            'page_title': u'Задачи все',
            'list_name': self.LIST_ALL,
            'show_performer': True,
            'show_due_date': True,
        })
        return context


class TaskDetail(UpdateView):
    model = Task
    # form_class = TaskForm
    template_name = 'task/task_detail.html'
    # success_url = '/tasks/'

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
        if obj.template.performer == self.request.user or \
           obj.template.author == self.request.user:
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
        if template_form.is_valid():
            task = self.get_object()
            task_tpl = template_form.save(commit=False)
            files_formset = self.get_files_formset()
            if files_formset.is_valid():
                task = form.save(commit=True)
                task_tpl = template_form.save(commit=True)
                files_formset.save()
            else:
                is_invalid_formset = False
        else:
            return self.form_invalid(form)

        # TODO переименовать переменную да и вообще с ней порядок навести
        if is_invalid_formset:
            task_saved.send(sender=Task, task=task, created=False, request=self.request)
            if task.deleted:
                messages.info(self.request, u'Задача "%s" удалена.' % task.template.title)
            else:
                messages.info(self.request, u'Задача "%s" сохранена.' % task.template.title)
            return super(TaskDetail, self).form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy('task:today_tasks_page'))


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

        if is_valid_formset:
            task = task_tpl.get_first_repeating_task()
            task_saved.send(sender=Task, task=task, created=True, request=self.request)
            messages.info(self.request, u'Создана задача "%s".' % task.template.title)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)


class TaskAddForm(TemplateFormMixin, CreateView):
    template_name = 'task/add_task_page.html'

    def get_success_url(self, *args, **kwargs):
        return self.request.GET.get('next', '/tasks/today/')


class CountTasks(View):
    def get(self, *args, **kwargs):
        today_count = TodayTasksPage.get_base_queryset_from_class(self.request).count()
        tomorrow_count = TomorrowTasksPage.get_base_queryset_from_class(self.request).count()
        overdue_count = OverdueTasksPage.get_base_queryset_from_class(self.request).count()
        later_count = LaterTasksPage.get_base_queryset_from_class(self.request).count()
        completed_count = CompletedTasksPage.get_base_queryset_from_class(self.request).count()
        inbound_count = InboundTasksPage.get_base_queryset_from_class(self.request).count()
        outbound_count = OutboundTasksPage.get_base_queryset_from_class(self.request).count()
        repeating_count = RepeatingTasksPage.get_base_queryset_from_class(self.request).count()
        all_count = AllTasksPage.get_base_queryset_from_class(self.request).count()
        context = {
            'today': today_count,
            'tomorrow': tomorrow_count,
            'overdue': overdue_count,
            'later': later_count,
            'completed': completed_count,
            'inbound': inbound_count,
            'outbound': outbound_count,
            'repeating': repeating_count,
            'all': all_count,
        }
        return JsonResponse(context)


class SetTaskStatus(View):
    def get(self, *args, **kwargs):
        task_pk = self.request.GET.get('task', None)
        new_status = self.request.GET.get('new_status', None)
        task = get_object_or_404(Task, pk=task_pk)
        if new_status in Task.STATUSES:
            task.status = new_status
            task.save()
            return HttpResponse('ok')
        return HttpResponse('error')
