# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy


@login_required
def front_page(request):
    # return render(request, 'core/page.html', {})
    return HttpResponseRedirect(reverse_lazy('notification:notifications_list_page'))
