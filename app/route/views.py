# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic import TemplateView

from app.route.models import BaseStep
from .forms import ChangeTextAuthorForm


class ChangeTextAuthorAction(FormView):
    form_class = ChangeTextAuthorForm
    template_name = 'route/action_form.html'
    success_url = '/tasks/'

    def get_form_kwargs(self):
        kwargs = super(ChangeTextAuthorAction, self).get_form_kwargs()
        step_id = self.request.GET.get('step')
        action_name = self.request.GET.get('action_name')
        step = BaseStep.objects.get(pk=step_id)
        kwargs.update({
            'request': self.request,
            'step': step,
            'action_name': action_name,
        })
        return kwargs
