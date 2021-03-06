# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from .views import (
    ContactsListPage,
    CompaniesListPage,
    ClientsListPage,
    ContactDetailPage,
    CompanyDetailPage,
    AddContactPage,
    AddCompanyPage,
)

urlpatterns = patterns('',
    url(r'^contacts/$', login_required(ContactsListPage.as_view()), name='contacts_list_page'),
    url(r'^companies/$', login_required(CompaniesListPage.as_view()), name='companies_list_page'),
    url(r'^company/(?P<pk>\d+)/$', login_required(CompanyDetailPage.as_view()), name='company_detail_page'),
    url(r'^clients/$', login_required(ClientsListPage.as_view()), name='clients_list_page'),
    url(r'^contact/(?P<pk>\d+)/$', login_required(ContactDetailPage.as_view()), name='contact_detail_page'),
    url(r'^add-contact/$', login_required(AddContactPage.as_view()), name='add_contact_page'),
    url(r'^add-company/$', login_required(AddCompanyPage.as_view()), name='add_company_page'),
)
