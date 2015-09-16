# -*- coding: utf-8 -*-
from django.views.generic.edit import FormView
from django.views.generic import View, UpdateView
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib.auth import authenticate, login
from endless_pagination.views import AjaxListView
from endless_pagination import settings as endless_settings
from django.views.decorators.csrf import csrf_exempt

from .models import Account, CompanyUnit
from .forms import CompanyUnitsListFilters, CompanyUnitForm


class Login(FormView):
    template_name = 'account/login.html'
    form_class = AuthenticationForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(Login, self).get_context_data(**kwargs)
        context['form'] = self.get_form(self.get_form_class())
        return context

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return super(Login, self).form_valid(form)
            else:
                return super(Login, self).form_invalid(form)
        else:
            return super(Login, self).form_invalid(form)


class EditProfile(UpdateView):
    model = Account
    fields = '__all__'


class CompanyUnitsListPage(AjaxListView):
    model = CompanyUnit
    template_name = 'account/company_unit/company_units_list_page.html'
    page_template = template_name
    context_object_name = 'tree'
    # TODO создать кастомый queryset
    # queryset = CompanyUnit.objects.filter(deleted=False)
    filters_form_class = CompanyUnitsListFilters

    def __init__(self, *args, **kwargs):
        super(CompanyUnitsListPage, self).__init__(*args, **kwargs)
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
        return CompanyUnit.objects.all().active()

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
        print CompanyUnit.objects.get_tree(filtered_ids=qs.values_list('pk', flat=True))
        return CompanyUnit.objects.get_tree(filtered_ids=qs.values_list('pk', flat=True))

    def get_context_data(self, **kwargs):
        # TODO брать из урла и переделать модуль endless_pagination, чтобы он использовал кол-во страниц из адреса или переменной вьюса.
        self.per_page = endless_settings.PER_PAGE

        context = super(CompanyUnitsListPage, self).get_context_data(**kwargs)
        self.define_filters()

        # фильтры списка
        context['filters_form'] = self.filters_form

        context['CompanyUnit'] = CompanyUnit

        # context['count_objects'] = self.queryset.count()
        from django.template import RequestContext
        return RequestContext(self.request, context)


class CompanyUnitDetailPage(UpdateView):
    model = CompanyUnit
    form_class = CompanyUnitForm
    template_name = 'account/company_unit/company_unit_detail_page.html'
    success_url = '/accounts/company_units/'

    def get_form_kwargs(self):
        kwargs = super(CompanyUnitDetailPage, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs
