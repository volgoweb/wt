# -*- coding: utf-8 -*-
import datetime
from django import forms
from django.shortcuts import get_object_or_404

from .models import *
from app.account.models import Account
from helper.forms import BootstrapFormMixin


class ApplicationForm(forms.Form):
    """
    Заявка на заказ каких-либо товаров от клиента.
    """
    application_desc = forms.CharField(widget=forms.Textarea, label=u'Описание')
    manager = forms.ModelChoiceField(queryset=Account.objects.all())
    # TODO добавить автовыбор исполнителем текущего авторизованного юзера

    def clean(self):
        self.cleaned_data = super(ApplicationForm, self).clean()

        route = Route(
            application_desc=self.cleaned_data.get('application_desc', ''),
            manager=self.cleaned_data.get('manager', ''),
        )
        route.save()

        step = route.get_step(name=Route.STEP_FIRST)
        step.run(**self.cleaned_data)
        # step.end(**self.cleaned_data)
