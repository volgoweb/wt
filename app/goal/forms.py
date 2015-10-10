# -*- coding: utf-8 -*-
from django import forms
# from datetimewidget.widgets import DateTimeWidget, DateWidget

from helper.forms import BootstrapFormMixin
from .models import Goal


class GoalForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Goal
        exclude = ['deleted']
        widgets = {
            'author': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(GoalForm, self).__init__(*args, **kwargs)
        if not getattr(self.instance, 'pk', None):
            self.fields['author'].initial = self.request.user
        else:
            if getattr(self.instance, 'author', None) != self.request.user:
                self.fields = {}

    def clean_author(self):
        self.cleaned_data['author'] = self.request.user
        return self.cleaned_data['author']
