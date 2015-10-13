# -*- coding: utf-8 -*-
from django import forms

from app.account.models import Account
from helper.forms import BootstrapFormMixin
from .models import SalesDeal, DealStatus
from app.contact.models import Company


class SalesDealForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = SalesDeal
        exclude = ['tasks', 'responsible']
        widgets = {
            'deleted': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SalesDealForm, self).__init__(*args, **kwargs)

        if 'author' in self.fields:
            self.fields['author'].initial = self.request.user
            self.fields['author'].widget = self.fields['author'].hidden_widget()

        if DealStatus.objects.filter(pk='new').exists():
            new_status = DealStatus.objects.get(pk='new')
            self.fields['status'].initial = new_status

    def clean_author(self, *args, **kwargs):
        return self.request.user


class SalesDealsFilters(BootstrapFormMixin, forms.Form):
    status = forms.ModelChoiceField(
        queryset=DealStatus.objects.all(),
        required=False,
        label=u'Статус',
    )
    responsible = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        required=False,
        label=u'Ответственный',
    )
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        required=False,
        label=u'Компания',
    )
