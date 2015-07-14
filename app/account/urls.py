# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from .views import (
    Login,
    EditProfile,
    CompanyUnitsListPage,
    CompanyUnitDetailPage,
)


urlpatterns = patterns('',
    url(r'^login/$', Login.as_view(), name='login'),
    #url(r'^(?P<slug>[^/]+)/$', 'main.portfolio.views.portfolio_detail_page', name='portfolio__portfolio_detail_page'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'front_page'}, name='logout'),
    url(r'^edit-profile/$', EditProfile.as_view(), name='edit_profile'),

    url(r'^company-units/$', CompanyUnitsListPage.as_view(), name='company_units_list_page'),
    url(r'^company-units/(?P<pk>\d+)/$', CompanyUnitDetailPage.as_view(), name='company_unit_detail_page'),
)
