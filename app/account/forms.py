# -*- coding: utf-8 -*-
from django import forms
from helper.forms import BootstrapFormMixin

from .models import CompanyUnit


class CompanyUnitsListFilters(BootstrapFormMixin, forms.Form):
    needle = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Найти по словам в названии или описании...'
        }),
    )


class CompanyUnitForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = CompanyUnit
        exclude = ['active']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CompanyUnitForm, self).__init__(*args, **kwargs)
