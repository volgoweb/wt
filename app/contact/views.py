# -*- coding: utf-8 -*-
from django.views.generic import ListView, UpdateView, CreateView
from django.db.models import Q
from django.forms.models import modelformset_factory
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponse
from endless_pagination.views import AjaxListView
from endless_pagination import settings as endless_settings
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS, FieldError

from .models import Contact, Company
from .forms import ContactsListFilters, ContactForm, CompanyForm, CompaniesListFilters


class ContactsListPage(AjaxListView):
    model = Contact
    template_name = 'contact/contacts_list_page.html'
    context_object_name = 'contacts'
    # TODO создать кастомый queryset
    # queryset = Contact.objects.filter(deleted=False)
    filters_form_class = ContactsListFilters

    def __init__(self, *args, **kwargs):
        super(ContactsListPage, self).__init__(*args, **kwargs)
        self.default_filters = {
            'needle': '',
            'contact_type': '',
        }

    def define_filters(self):
        data = {}
        for key, default_value in self.default_filters.items():
            if key in self.request.GET:
                data[key] = self.request.GET.get(key)
            else:
                data[key] = default_value

        self.filters_form = self.filters_form_class(data)
        self.filters_values = {}
        if self.filters_form.is_valid():
            for key in self.default_filters.keys():
                self.filters_values[key] = self.filters_form.cleaned_data.get(key)
        else:
            print '--------------- filters not valid'
            print self.filters_form.errors

    def get_base_queryset(self):
        return Contact.objects.filter(deleted=False).order_by('full_name')

    def get_queryset(self):
        qs = self.get_base_queryset()
        # if len(self.request.GET) > 0:
        self.define_filters()

        filter_needle = self.filters_values.get('needle')
        if filter_needle:
            qs = qs.filter(
                Q(full_name__icontains=filter_needle) |
                Q(desc__icontains=filter_needle) |
                Q(phone__icontains=filter_needle) |
                Q(mobile_phone__icontains=filter_needle) |
                Q(email__icontains=filter_needle)
            )

        filter_contact_type = self.filters_values.get('contact_type')
        if filter_contact_type == self.filters_form.CONTACT_TYPE_LEAD:
            qs = qs.filter(is_lead=True)
        elif filter_contact_type == self.filters_form.CONTACT_TYPE_CLIENT:
            qs = qs.filter(is_client=True)
        elif filter_contact_type == self.filters_form.CONTACT_TYPE_PARTNER:
            qs = qs.filter(is_partner=True)

        self.queryset = qs
        return qs

    def get_context_data(self, **kwargs):
        # TODO брать из урла и переделать модуль endless_pagination, чтобы он использовал кол-во страниц из адреса или переменной вьюса.
        self.per_page = endless_settings.PER_PAGE

        context = super(ContactsListPage, self).get_context_data(**kwargs)
        self.define_filters()

        # фильтры списка
        context['filters_form'] = self.filters_form

        # context['count_objects'] = self.queryset.count()
        from django.template import RequestContext
        return RequestContext(self.request, context)

    def get_page_template(self, *args, **kwargs):
        return 'contact/contacts_list.html'


class ClientsListPage(ContactsListPage):
    def get_base_queryset(self):
        return Contact.objects.filter(deleted=False, is_client=True).order_by('full_name')


class ContactDetailPage(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact/contact_detail_page.html'
    success_url = '/contacts/'

    def get_form_kwargs(self):
        kwargs = super(ContactDetailPage, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs


class AddContactPage(CreateView):
    model = Contact
    template_name = 'contact/add_contact_page.html'
    form_class = ContactForm
    success_url = '/contacts/'

    def get_form_kwargs(self):
        kwargs = super(AddContactPage, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs


class CompaniesListPage(AjaxListView):
    model = Company
    template_name = 'contact/companies_list_page.html'
    context_object_name = 'companies'
    # TODO создать кастомый queryset
    # queryset = Company.objects.filter(deleted=False)
    filters_form_class = CompaniesListFilters

    def __init__(self, *args, **kwargs):
        super(CompaniesListPage, self).__init__(*args, **kwargs)
        self.default_filters = {
            'needle': '',
        }

    def define_filters(self):
        data = {}
        for key, default_value in self.default_filters.items():
            if key in self.request.GET:
                data[key] = self.request.GET.get(key)
            else:
                data[key] = default_value

        self.filters_form = self.filters_form_class(data)
        self.filters_values = {}
        if self.filters_form.is_valid():
            for key in self.default_filters.keys():
                self.filters_values[key] = self.filters_form.cleaned_data.get(key)
        else:
            print '--------------- filters not valid'
            print self.filters_form.errors

    def get_base_queryset(self):
        return Company.objects.filter(deleted=False).order_by('name')

    def get_queryset(self):
        qs = self.get_base_queryset()
        # if len(self.request.GET) > 0:
        self.define_filters()

        filter_needle = self.filters_values.get('needle')
        if filter_needle:
            qs = qs.filter(
                Q(name__icontains=filter_needle) |
                Q(desc__icontains=filter_needle) |
                Q(phone__icontains=filter_needle) |
                Q(mobile_phone__icontains=filter_needle) |
                Q(email__icontains=filter_needle)
            )

        filter_contact_type = self.filters_values.get('company_type')
        if filter_contact_type == self.filters_form.CONTACT_TYPE_LEAD:
            qs = qs.filter(is_lead=True)
        elif filter_contact_type == self.filters_form.CONTACT_TYPE_CLIENT:
            qs = qs.filter(is_client=True)
        elif filter_contact_type == self.filters_form.CONTACT_TYPE_PARTNER:
            qs = qs.filter(is_partner=True)

        self.queryset = qs
        return qs

    def get_context_data(self, **kwargs):
        # TODO брать из урла и переделать модуль endless_pagination, чтобы он использовал кол-во страниц из адреса или переменной вьюса.
        self.per_page = endless_settings.PER_PAGE

        context = super(CompaniesListPage, self).get_context_data(**kwargs)
        self.define_filters()

        # фильтры списка
        context['filters_form'] = self.filters_form

        # context['count_objects'] = self.queryset.count()
        from django.template import RequestContext
        return RequestContext(self.request, context)

    def get_page_template(self, *args, **kwargs):
        return 'contact/companies_list.html'


class CompanyDetailPage(UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'contact/company_detail_page.html'
    success_url = '/contacts/'

    def get_form_kwargs(self):
        kwargs = super(CompanyDetailPage, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs


class AddCompanyPage(CreateView):
    model = Company
    template_name = 'contact/add_contact_page.html'
    form_class = CompanyForm
    success_url = '/contacts/'

    def get_form_kwargs(self):
        kwargs = super(AddCompanyPage, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs
