# -*- coding: utf-8 -*-
from collections import OrderedDict

from django import forms

from helper.forms import BootstrapFormMixin
from .models import Contact, Company


class ContactsListFilters(BootstrapFormMixin, forms.Form):
    CONTACT_TYPE_LEAD = 'is_lead'
    CONTACT_TYPE_CLIENT = 'is_client'
    CONTACT_TYPE_PARTNER = 'is_partner'
    CONTACT_TYPE_CHOICES = OrderedDict([
        (CONTACT_TYPE_LEAD, u'Лид'),
        (CONTACT_TYPE_CLIENT, u'Клиент'),
        (CONTACT_TYPE_PARTNER, u'Партнер'),
    ])
    needle = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Поиск'
        }),
        label='',
    )
    contact_type = forms.ChoiceField(
        choices=[('', '---------')] + CONTACT_TYPE_CHOICES.items(),
        required=False,
        label=u'Тип контакта',
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
        if self.request.GET.get('is_lead'):
            self.fields['is_lead'].initial = True

    def clean_author(self):
        self.cleaned_data['author'] = self.request.user
        return self.cleaned_data['author']

    def clean(self):
        self.cleaned_data = super(ContactForm, self).clean()
        if not self.cleaned_data['phone'] and not self.cleaned_data['mobile_phone']:
            raise forms.ValidationError({
                'phone': u'Укажите либо телефон либо мобильный телефон.',
                'mobile_phone': u'Укажите либо телефон либо мобильный телефон.',
            })
        return self.cleaned_data


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


class CompaniesListFilters(ContactsListFilters):
    pass
