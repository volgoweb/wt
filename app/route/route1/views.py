# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from django.views.generic import ListView
from django.views.generic.edit import FormView

# from app.task.forms import TaskForm
from .forms import ApplicationForm


def test(request):
    return render_to_response('blaaaaaaaaaa')


class StartRoute(FormView):
    form_class = ApplicationForm
    template_name = 'route/route1/application_form.html'
    success_url = '/tasks/'
