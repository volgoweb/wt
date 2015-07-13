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

from .models import Partner
from .forms import PartnersListFilters, PartnerForm


class PartnersListPage(AjaxListView):
    model = Partner
    template_name = 'partner/partners_list_page.html'
    context_object_name = 'partners'
    # TODO создать кастомый queryset
    # queryset = Partner.objects.filter(deleted=False)
    filters_form_class = PartnersListFilters

    def __init__(self, *args, **kwargs):
        super(PartnersListPage, self).__init__(*args, **kwargs)
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

    def get_base_queryset(self):
        return Partner.objects.filter(deleted=False)

    def get_queryset(self):
        qs = self.get_base_queryset()
        # if len(self.request.GET) > 0:
        self.define_filters()

        filter_needle = self.filters_values.get('needle')
        if filter_needle:
            qs = qs.filter(
                Q(name__icontains=filter_needle) |
                Q(desc__icontains=filter_needle)
            )

        self.queryset = qs
        return qs

    def get_context_data(self, **kwargs):
        # TODO брать из урла и переделать модуль endless_pagination, чтобы он использовал кол-во страниц из адреса или переменной вьюса.
        self.per_page = endless_settings.PER_PAGE

        context = super(PartnersListPage, self).get_context_data(**kwargs)
        self.define_filters()

        # фильтры списка
        context['filters_form'] = self.filters_form

        # context['count_objects'] = self.queryset.count()
        from django.template import RequestContext
        return RequestContext(self.request, context)


class PartnerDetailPage(UpdateView):
    model = Partner
    form_class = PartnerForm
    template_name = 'partner/partner_detail_page.html'
    success_url = '/partners/'

    def get_form_kwargs(self):
        kwargs = super(PartnerDetailPage, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs


class AddPartnerPage(CreateView):
    model = Partner
    template_name = 'partner/add_partner_page.html'
    form_class = PartnerForm
    success_url = '/partners/'

    def get_form_kwargs(self):
        kwargs = super(AddPartnerPage, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs
