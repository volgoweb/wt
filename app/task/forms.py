# -*- coding: utf-8 -*-
import datetime
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
from app.account.models import Account, CompanyUnit
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
            # 'date': DateTimeWidget(
            #     usel10n=True,
            #     bootstrap_version=3,
            #     options={
            #         'format': 'dd.mm.yyyy hh:ii',
            #         'autoclose': True,
            #         'showMeridian' : True
            #     },
            # ),
        }


class AddTaskForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['template']
        # fields = ['title', 'desc', 'status']
        widgets = {
            # 'due_date': DateTimeWidget(
            #     usel10n=True,
            #     bootstrap_version=3,
            #     options={
            #         'format': 'dd.mm.yyyy hh:ii',
            #         'autoclose': True,
            #         'showMeridian' : True
            #     },
            # ),
            'status': forms.widgets.RadioSelect(),
            'is_repeating_clone': forms.HiddenInput(),
            'deleted': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.can_edit = kwargs.pop('can_edit', None)
        self.is_shortform = kwargs.pop('is_shortform', None)
        super(AddTaskForm, self).__init__(*args, **kwargs)

        if 'author' in self.fields:
            self.fields['author'].initial = self.request.user
            self.fields['author'].widget = self.fields['author'].hidden_widget()
        if 'status' in self.fields:
            self.fields['status'].widget = forms.widgets.HiddenInput()

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
    def __init__(self, *args, **kwargs):
        # self.Meta.widgets['status'] = forms.widgets.RadioSelect()
        super(TaskForm, self).__init__(*args, **kwargs)
        self.filter_fields(can_edit=self.can_edit)
        self.fields['status'].widget = forms.widgets.RadioSelect(choices=self.fields['status'].choices)

        task_pk = getattr(self.instance, 'pk', None)
        if task_pk:
            performer = self.instance.template.performer
            if performer and self.request.user != self.instance.author:
                for fname in self.fields:
                    if fname not in ('status',):
                        del(self.fields[fname])

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
    search = forms.CharField(
        required=False,
        label=u'Название/описание',
    )
    performer = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        required=False,
        label=TaskTemplate.performer.field.verbose_name,
    )
    author = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        required=False,
        label=TaskTemplate.author.field.verbose_name,
    )
    status = forms.ChoiceField(
        choices=[('', '---------')]+Task.STATUSES.items(),
        required=False,
        label=u'Статус',
    )


class TaskTemplateForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = TaskTemplate
        exclude = ['step_id', 'step_type', 'files', 'task_steps']
        widgets = {
            # 'due_date': DateTimeWidget(
            #     usel10n=True,
            #     bootstrap_version=3,
            #     options={
            #         'format': 'dd.mm.yyyy hh:ii',
            #         'autoclose': True,
            #         'showMeridian' : True
            #     },
            # ),
            'performer': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.task = kwargs.pop('task', None)
        self.can_edit = kwargs.pop('can_edit', None)
        self.is_shortform = kwargs.pop('is_shortform', None)

        # self.Meta.widgets['status'] = forms.widgets.HiddenInput()

        super(TaskTemplateForm, self).__init__(*args, **kwargs)
        self.instance.request = self.request
        tpl_pk = getattr(self.instance, 'pk', None)
        if tpl_pk:
            performer = getattr(self.instance, 'performer', None)
            if performer and self.request.user != self.instance.get_first_repeating_task().author and self.request.user != self.instance.performer:
                self.fields = {}
        else:
            self.fields['performer'].initial = self.request.user
            self.fields['performer_unit'].initial = self.request.user.job
        if 'performer_unit' in self.fields:
            self.fields['performer_unit'].queryset = CompanyUnit.objects.all().employee()
            choices = [(o.pk, u'{0} ({1})'.format(o.get_user() or '', o.name)) for o in self.fields['performer_unit'].queryset]
            choices.sort(key=lambda x: x[1])
            self.fields['performer_unit'].widget.choices = [('', '----------')] + choices

        if self.task and 'due_date' in self.fields:
            self.fields['due_date'].widget = self.fields['due_date'].hidden_widget()

        if 'author' in self.fields:
            self.fields['author'].initial = self.request.user
            self.fields['author'].widget = self.fields['author'].hidden_widget()

        if 'title' in self.fields:
            self.fields['title'].widget.attrs.update({
                'autofocus': '',
            })
            if self.is_shortform:
                self.fields['title'].widget.attrs.update({
                    'placeholder': u'Введите название новой задачи и нажмите Enter ...',
                    'title': u'Введите название новой задачи и нажмите Enter',
                })
                self.fields['due_date'].widget.attrs.update({
                    'placeholder': u'Срок',
                })
                self.fields['due_date'].initial = datetime.datetime.now() + datetime.timedelta(minutes=30)

        goal_pk = self.request.GET.get('goal', None)
        if goal_pk and 'goal' in self.fields:
            self.fields['goal'].initial = goal_pk

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

    def clean(self):
        self.cleaned_data = super(TaskTemplateForm, self).clean()
        due_date = self.cleaned_data.get('due_date')
        if self.cleaned_data.get('period') and not due_date:
            raise forms.ValidationError({'due_date': u'Крайний срок обязателен при выбранном периоде повторения.'})

        performer_unit = self.cleaned_data['performer_unit']
        if performer_unit:
            performer_user = performer_unit.get_user()
            if performer_user:
                self.cleaned_data['performer'] = performer_user
        return self.cleaned_data
