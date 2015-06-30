# -*- coding: utf-8 -*-
from django.shortcuts import render
from endless_pagination.views import AjaxListView
from endless_pagination import settings as endless_settings
from django.views.decorators.csrf import csrf_exempt

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
        'readed': '',
    }

    # @csrf_exempt
    # def get(self, *args, **kwargs):
    #     return super(NotificationsListPage, self).get(*args, **kwargs)

    # def define_filters(self):
    #     # TODO вынести в отдельный миксин
    #     if len(self.request.GET) > 0:
    #         self.filters_form = self.filters_form_class(self.request.GET, prefix='notifications_filters')
    #     else:
    #         self.filters_form = self.filters_form_class(initial=self.default_filters, prefix='notifications_filters')
    #     self.filters_values = {}
    #     if self.filters_form.is_valid():
    #         for key in self.default_filters.keys():
    #             self.filters_values[key] = self.filters_form.cleaned_data.get(key)

    def get_queryset(self):
        qs = Notification.objects.filter(subscriber=self.request.user)
    #     if len(self.request.GET) > 0:
    #         self.define_filters()

    #         filter_readed = self.filters_values.get('readed')
    #         if filter_readed:
    #             qs = qs.filter(readed=filter_readed)

        return qs

    # def get_context_data(self, **kwargs):
    #     # TODO вынести в отдельный миксин
    #     # TODO брать из урла и переделать модуль endless_pagination, чтобы он использовал кол-во страниц из адреса или переменной вьюса.
    #     self.per_page = endless_settings.PER_PAGE

    #     context = super(NotificationsListPage, self).get_context_data(**kwargs)
    #     self.define_filters()

    #     # фильтры списка
    #     context['filters_form'] = self.filters_form
    #     return context
