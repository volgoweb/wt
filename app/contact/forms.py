# -*- coding: utf-8 -*-
from django import forms
from helper.forms import BootstrapFormMixin

from .models import Contact, Company


class ContactsListFilters(BootstrapFormMixin, forms.Form):
    needle = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Поиск'
        }),
        label='',
    )


class ContactForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ['deleted']
        widgets = {
            'author': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['author'].initial = self.request.user

    def clean_author(self):
        self.cleaned_data['author'] = self.request.user
        return self.cleaned_data['author']



class CompanyForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['deleted']
        widgets = {
            'author': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CompanyForm, self).__init__(*args, **kwargs)
        self.fields['author'].initial = self.request.user

    def clean_author(self):
        self.cleaned_data['author'] = self.request.user
        return self.cleaned_data['author']

