# -*- coding: utf-8 -*-
from django import forms
# from django.core.exceptions import ValidationError
# from django.template.loader import render_to_string
# from django.forms.models import modelformset_factory
# from ckeditor.widgets import CKEditorWidget
from django.forms.models import modelformset_factory
from django.template.loader import render_to_string
from datetimewidget.widgets import DateTimeWidget
from ajax_upload.widgets import AjaxClearableFileInput

from .models import *
from helper.forms import BootstrapFormMixin
from helper.fields import FormsetField
from app.account.models import Account
from app.core.models import FileItem

class TaskStepForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = TaskStep
        fields = '__all__'
        widgets = {
            'date': DateTimeWidget(
                usel10n=True,
                bootstrap_version=3,
                options={
                    'format': 'dd.mm.yyyy hh:ii',
                    'autoclose': True,
                    'showMeridian' : True
                },
            ),
        }


class AddTaskForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['step_id', 'step_type', 'deleted', 'files', 'comments', 'task_steps']
        # fields = ['title', 'desc', 'status']
        widgets = {
            'due_date': DateTimeWidget(
                usel10n=True,
                bootstrap_version=3,
                options={
                    'format': 'dd.mm.yyyy hh:ii',
                    'autoclose': True,
                    'showMeridian' : True
                },
            ),
            'status': forms.widgets.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.can_edit = kwargs.pop('can_edit', None)

        # self.Meta.widgets['status'] = forms.widgets.HiddenInput()

        super(AddTaskForm, self).__init__(*args, **kwargs)
        self.instance.request = self.request
        if 'author' in self.fields:
            self.fields['author'].initial = self.request.user
            self.fields['author'].widget = self.fields['author'].hidden_widget()
        if 'status' in self.fields:
            self.fields['status'].widget = forms.widgets.HiddenInput()
        if 'title' in self.fields:
            self.fields['title'].widget.attrs.update({
                'autofocus': '',
            })

        self.add_files_formset()
        # self.add_task_steps_formset()

    def add_files_formset(self, *args, **kwargs):
        extra = 1
        qs = None
        if getattr(self.instance, 'pk', None):
            qs = self.instance.files.all()
            if qs.count() > 0:
                extra = 0
        Formset = modelformset_factory(
            FileItem,
            fields=['file'],
            widgets={'file': AjaxClearableFileInput()},
            extra=extra,
            can_delete=True,
        )
        formset = Formset(data=self.request.POST or None, files=self.request.FILES or None, queryset=qs)
        self.files_formset = formset
        self.fields['files_formset'] = FormsetField(
            formset=render_to_string('task/task_detail/files_formset.html', {'files_formset': formset}),
            label=u'Файлы',
        )

    def add_task_steps_formset(self, *args, **kwargs):
        extra = 1
        qs = None
        if getattr(self.instance, 'pk', None):
            qs = self.instance.task_steps.all()
            if qs.count() > 0:
                extra = 0
        Formset = modelformset_factory(TaskStep,
            form=TaskStepForm,
            extra=extra,
            can_delete=True,
        )
        formset = Formset(self.request.POST or None, queryset=qs)
        self.task_steps_formset = formset
        self.fields['task_steps_formset'] = FormsetField(
            formset=render_to_string('task/task_detail/task_steps_formset.html', {'task_steps_formset': formset}),
            label=u'Шаги',
        )

    def clean_author(self, *args, **kwargs):
        return self.request.user

    def save(self, *args, **kwargs):
        result = super(AddTaskForm, self).save(*args, **kwargs)
        # TODO подумать как можно вынести сохранение формсета в класс поля.
        if self.files_formset.is_valid():
            items = self.files_formset.save()
            for item in items:
                self.instance.files.add(item)

        # if self.task_steps_formset.is_valid():
        #     items = self.task_steps_formset.save()
        #     for item in items:
        #         self.instance.task_steps.add(item)
        return result


class TaskForm(AddTaskForm):
    class Meta:
        model = Task
        exclude = AddTaskForm.Meta.exclude + ['title', 'desc', 'performer', 'due_date']
        widgets = AddTaskForm.Meta.widgets

    def __init__(self, *args, **kwargs):
        # self.Meta.widgets['status'] = forms.widgets.RadioSelect()
        super(TaskForm, self).__init__(*args, **kwargs)
        self.filter_fields(can_edit=self.can_edit)
        self.fields['status'].widget = forms.widgets.RadioSelect(choices=self.fields['status'].choices)

    def filter_fields(self, can_edit=False):
        if not can_edit:
            for f in self.fields.values():
                f.widget = f.hidden_widget()


class TasksListFilters(BootstrapFormMixin, forms.Form):
    # TODO подумать, можно ли как-то ограничить список,
    # чтобы в нем были лишь сотрудники, задачи которых
    # авторизованный пользователь имеет право смотреть... 
    # ну либо те сотрудники, на которых висят задачи.
    # TODO добавить значение "я"
    performer = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        required=False,
        label=Task.performer.field.verbose_name,
    )
    status = forms.ChoiceField(
        choices=[('', '---------')]+Task.STATUSES.items(),
        required=False,
        label=u'Статус',
    )
