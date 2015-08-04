# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from .views import (
    SalesDealsListPage,
    SalesDealDetail,
    SalesDealAddPage,
)

urlpatterns = patterns('',
    url(r'^sales-deals$', SalesDealsListPage.as_view(), name='sales_deals_list_page'),
    url(r'^sales-deal/(?P<pk>\d+)/$', login_required(SalesDealDetail.as_view()), name='sales_deal_detail_page'),
    url(r'^sales-deal/add/$', login_required(SalesDealAddPage.as_view()), name='sales_deal_add_page'),
)
