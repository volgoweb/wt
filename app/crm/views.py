# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView
from django.forms.models import modelformset_factory
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponse
from endless_pagination.views import AjaxListView
from endless_pagination import settings as endless_settings
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS, FieldError
from django.core.urlresolvers import reverse_lazy

from .models import SalesDeal
from .forms import SalesDealsFilters, SalesDealForm

class SalesDealsListPage(AjaxListView):
    model = SalesDeal
    template_name = 'crm/sales_deals_list_page.html'
    context_object_name = 'deals'
    filters_form_class = SalesDealsFilters

    def __init__(self, *args, **kwargs):
        super(SalesDealsListPage, self).__init__(*args, **kwargs)
        self.default_filters = {
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
        return self.model.objects.all()

    def get_queryset(self):
        qs = self.get_base_queryset()
        self.define_filters()

        # filter_performer = self.filters_values.get('performer')
        # if filter_performer:
        #     qs = qs.filter(template__performer=filter_performer)

        self.queryset = qs
        return qs

    def get_page_template(self, *args, **kwargs):
        return 'crm/sales_deals_list_block.html'

    def get_context_data(self, **kwargs):
        # TODO брать из урла и переделать модуль endless_pagination, чтобы он использовал кол-во страниц из адреса или переменной вьюса.
        self.per_page = endless_settings.PER_PAGE

        context = super(SalesDealsListPage, self).get_context_data(**kwargs)
        self.define_filters()

        # фильтры списка
        context['filters_form'] = self.filters_form

        # context['count_objects'] = self.queryset.count()
        from django.template import RequestContext
        return RequestContext(self.request, context)


class SalesDealDetail(UpdateView):
    model = SalesDeal
    template_name = 'crm/sales_deal_form.html'
    form_class = SalesDealForm

    def get_form_kwargs(self):
        kwargs = super(SalesDealDetail, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def get_success_url(self):
        return self.request.GET.get('next', '/crm/')

class SalesDealAddPage(CreateView):
    model = SalesDeal
    template_name = 'crm/sales_deal_form.html'
    form_class = SalesDealForm

    def get_form_kwargs(self):
        kwargs = super(SalesDealAddPage, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def get_success_url(self):
        return self.request.GET.get('next', '/crm/')
