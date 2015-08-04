# -*- coding: utf-8 -*-
from django import forms

from helper.forms import BootstrapFormMixin
from .models import SalesDeal, DealStatus


class SalesDealForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = SalesDeal
        exclude = ['tasks', 'deleted', 'responsible']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SalesDealForm, self).__init__(*args, **kwargs)

        if 'author' in self.fields:
            self.fields['author'].initial = self.request.user
            self.fields['author'].widget = self.fields['author'].hidden_widget()

    def clean_author(self, *args, **kwargs):
        return self.request.user


class SalesDealsFilters(BootstrapFormMixin, forms.Form):
    status = forms.ModelChoiceField(
        queryset=DealStatus.objects.all(),
        required=False,
        label=u'Статус',
    )
