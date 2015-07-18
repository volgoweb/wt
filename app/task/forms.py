# -*- coding: utf-8 -*-
from django import forms
# from django.core.exceptions import ValidationError
# from django.template.loader import render_to_string
# from django.forms.models import modelformset_factory
# from ckeditor.widgets import CKEditorWidget
from django.forms.models import modelformset_factory, inlineformset_factory
from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.template.loader import render_to_string
from datetimewidget.widgets import DateTimeWidget
from ajax_upload.widgets import AjaxClearableFileInput

from .models import *
from helper.forms import BootstrapFormMixin
from helper.fields import FormsetField
from app.account.models import Account
from app.core.models import FileItem
from app.core.forms import FileItemForm


class TaskFileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = TaskFile
        fields = '__all__'
        widgets = {
            'file': AjaxClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        super(TaskFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False


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
        exclude = ['step_id', 'step_type', 'deleted', 'comments', 'task_steps', 'files', 'periodic_task']
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
        if not getattr(self.instance, 'pk', None):
            self.fields['performer'].initial = self.request.user
        if 'author' in self.fields:
            self.fields['author'].initial = self.request.user
            self.fields['author'].widget = self.fields['author'].hidden_widget()
        if 'status' in self.fields:
            self.fields['status'].widget = forms.widgets.HiddenInput()
        if 'title' in self.fields:
            self.fields['title'].widget.attrs.update({
                'autofocus': '',
                'placeholder': u'Введите название новой задачи и нажмите Enter ...',
                'title': u'Введите название новой задачи и нажмите Enter',
            })

        # self.add_files_formset()
        # self.add_task_steps_formset()

    def add_files_formset(self, *args, **kwargs):
        extra = 1
        qs = TaskFile.objects.none()
        if getattr(self.instance, 'pk', None):
            # qs = TaskFile.objects.filter(owner_id=self.instance.pk)
            qs = self.instance.files.all()
            if qs.count() > 0:
                extra = 0
        Formset = modelformset_factory(
            # Task,
            TaskFile,
            form=TaskFileForm,
            # ct_field='owner_type',
            # fk_field='owner_id',
            fields=['file'],
            # widgets={'file': AjaxClearableFileInput()},
            extra=extra,
            can_delete=True,
        )
        self.FilesFormset = Formset
        formset = Formset(data=self.request.POST or None, files=self.request.FILES or None, queryset=qs)
        # forms = formset.forms
        # assert False
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

    # def save(self, *args, **kwargs):
    #     task = super(AddTaskForm, self).save(*args, **kwargs)
    #     if self.files_formset.is_valid():
    #         items = self.files_formset.save()
    #         self.instance.files.add(*items)
    #         self.instance.save()
    #         print 'items'
    #         print items
    #         # self.instance.files.add(*items)
    #     else:
    #         err = self.files_formset.errors
    #         print '--------- files_formset  errors:'
    #         print err

    #     # if self.task_steps_formset.is_valid():
    #     #     items = self.task_steps_formset.save()
    #     #     for item in items:
    #     #         self.instance.task_steps.add(item)
    #     return task


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
