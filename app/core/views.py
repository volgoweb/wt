# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required


@login_required
def front_page(request):
    return render(request, 'core/page.html', {})
