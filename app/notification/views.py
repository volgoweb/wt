# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from endless_pagination.views import AjaxListView
from endless_pagination import settings as endless_settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.views.generic import View

from .models import Notification
from .forms import NotificationsListFilters


class NotificationsListPage(AjaxListView):
    model = Notification
    template_name = 'notification/notifications_list_page.html'
    context_object_name = 'notifications'
    # TODO создать кастомый queryset
    # queryset = Task.objects.filter(deleted=False)
    filters_form_class = NotificationsListFilters
    default_filters = {
        'readed': 'unreaded',
    }

    # @csrf_exempt
    # def get(self, *args, **kwargs):
    #     return super(NotificationsListPage, self).get(*args, **kwargs)

    def define_filters(self):
        # TODO вынести в отдельный миксин
        if len(self.request.GET) > 0:
            self.filters_form = self.filters_form_class(self.request.GET)
        else:
            self.filters_form = self.filters_form_class(self.default_filters)
        self.filters_values = {}
        if self.filters_form.is_valid():
            for key in self.default_filters.keys():
                self.filters_values[key] = self.filters_form.cleaned_data.get(key)
        else:
            print '------------ notif form invalid'
            print self.filters_form.errors

    def get_queryset(self):
        qs = Notification.objects.filter(subscriber=self.request.user).select_related('subscriber')
        self.define_filters()

        filter_readed = self.filters_values.get('readed')
        if filter_readed == 'unreaded':
            qs = qs.filter(readed=False)

        return qs

    def get_context_data(self, **kwargs):
        # TODO вынести в отдельный миксин
        # TODO брать из урла и переделать модуль endless_pagination, чтобы он использовал кол-во страниц из адреса или переменной вьюса.
        self.per_page = endless_settings.PER_PAGE

        context = super(NotificationsListPage, self).get_context_data(**kwargs)
        self.define_filters()

        # фильтры списка
        context['filters_form'] = self.filters_form
        return context


class CountNotifications(View):
    def get(self, *args, **kwargs):
        qs_all = Notification.objects.filter(subscriber=self.request.user)
        qs_unreaded = qs_all.filter(readed=False)
        return JsonResponse({
            'all': qs_all.count(),
            'unreaded': qs_unreaded.count(),
        })


@login_required
def set_readed(request, pk):
    n = get_object_or_404(Notification, pk=pk)
    readed = request.GET.get('readed')
    if readed:
        n.readed = True
    else:
        n.readed = False
    n.save()
    return HttpResponse('ok')

