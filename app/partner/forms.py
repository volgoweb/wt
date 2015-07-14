# -*- coding: utf-8 -*-
from django import forms
from helper.forms import BootstrapFormMixin

from .models import Partner


class PartnersListFilters(BootstrapFormMixin, forms.Form):
    needle = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Найти по словам в названии или описании...'
        }),
    )


class PartnerForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Partner
        exclude = ['deleted']
        widgets = {
            'author': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PartnerForm, self).__init__(*args, **kwargs)
        self.fields['author'].initial = self.request.user

    def clean_author(self):
        self.cleaned_data['author'] = self.request.user
        return self.cleaned_data['author']
