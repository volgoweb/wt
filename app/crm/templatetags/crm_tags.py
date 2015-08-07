# -*- coding: utf-8 -*-
from django import template
# from django.core.urlresolvers import reverse
from app.crm.models import SalesDeal, DealStatus

register = template.Library()

@register.inclusion_tag('crm/deals_statistics.html', takes_context = True)
def my_deals_statistics(context):
    request = context.get('request', None)
    statistics = []
    if request:
        counts = SalesDeal.objects.count_of_responisble_by_status(request.user)
        for status_item in DealStatus.objects.all():
            statistics.append({
                'title': status_item.title,
                'count': counts.get(status_item.pk, ''),
            })
    return {
        'statistics': statistics,
    }


