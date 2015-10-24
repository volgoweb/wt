# -*- coding: utf-8 -*-
from django.views.generic import UpdateView, CreateView, DetailView
# from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from endless_pagination.views import AjaxListView
from endless_pagination import settings as endless_settings
from django.core.urlresolvers import reverse_lazy

from .models import Idea
from .signals import idea_saved
from .forms import IdeaForm


class IdeasListPage(AjaxListView):
    model = Idea
    template_name = 'idea/ideas_list_page.html'
    context_object_name = 'ideas'
    # TODO создать кастомый queryset
    # queryset = Idea.objects.filter(deleted=False)
    # filters_form_class = IdeasListFilters

    # def __init__(self, *args, **kwargs):
    #     super(IdeasListPage, self).__init__(*args, **kwargs)
    #     self.default_filters = {
    #         'needle': '',
    #     }

    # def define_filters(self):
    #     data = {}
    #     for key, default_value in self.default_filters.items():
    #         if key in self.request.GET:
    #             data[key] = self.request.GET.get(key)
    #         else:
    #             data[key] = default_value

    #     self.filters_form = self.filters_form_class(data)
    #     self.filters_values = {}
    #     if self.filters_form.is_valid():
    #         for key in self.default_filters.keys():
    #             self.filters_values[key] = self.filters_form.cleaned_data.get(key)

    def get_base_queryset(self):
        return Idea.objects.filter(deleted=False).order_by('created')

    def get_queryset(self):
        qs = self.get_base_queryset()
        # if len(self.request.GET) > 0:
        # self.define_filters()

        # filter_needle = self.filters_values.get('needle')
        # if filter_needle:
        #     qs = qs.filter(
        #         Q(full_name__icontains=filter_needle) |
        #         Q(desc__icontains=filter_needle) |
        #         Q(phone__icontains=filter_needle) |
        #         Q(mobile_phone__icontains=filter_needle)
        #     )

        self.queryset = qs
        return qs

    def get_context_data(self, **kwargs):
        # TODO брать из урла и переделать модуль endless_pagination, чтобы он использовал кол-во страниц из адреса или переменной вьюса.
        self.per_page = endless_settings.PER_PAGE

        context = super(IdeasListPage, self).get_context_data(**kwargs)
        # self.define_filters()

        # фильтры списка
        # context['filters_form'] = self.filters_form

        # context['count_objects'] = self.queryset.count()
        from django.template import RequestContext
        return RequestContext(self.request, context)

    def get_page_template(self, *args, **kwargs):
        return 'idea/ideas_list.html'


class IdeaEditPage(UpdateView):
    model = Idea
    form_class = IdeaForm
    template_name = 'idea/idea_form_page.html'
    success_url = '/ideas/'

    def get_object(self, *args, **kwargs):
        obj = super(IdeaEditPage, self).get_object(*args, **kwargs)
        if obj.deleted:
            raise Http404(u'Эта идея удалена!')
        return obj

    def get_form_kwargs(self):
        kwargs = super(IdeaEditPage, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def form_valid(self, form, *args, **kwargs):
        result = super(IdeaEditPage, self).form_valid(form, *args, **kwargs)
        idea_saved.send(sender=Idea, idea=self.object, created=False, request=self.request)
        return result


class IdeaDetailPage(DetailView):
    model = Idea
    slug_field = 'pk'
    slug_url_kwarg = 'pk'
    context_object_name = 'idea'
    template_name = 'idea/idea_detail_page.html'


class AddIdeaPage(CreateView):
    model = Idea
    template_name = 'idea/idea_form_page.html'
    form_class = IdeaForm
    # success_url = '/ideas/my-ideas/'

    def get_form_kwargs(self):
        kwargs = super(AddIdeaPage, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def form_valid(self, form, *args, **kwargs):
        idea = form.save()
        idea_saved.send(sender=Idea, idea=idea, created=True, request=self.request)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('idea:ideas_list_page')
