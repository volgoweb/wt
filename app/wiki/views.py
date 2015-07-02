# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from endless_pagination.views import AjaxListView
from endless_pagination import settings as endless_settings
from django.views.decorators.csrf import csrf_exempt

from .models import WikiPage
from .forms import WikiListFilters, WikiPageForm

class WikiList(AjaxListView):
    model = WikiPage
    template_name = 'wiki/wiki_list_page.html'
    context_object_name = 'pages'
    # TODO создать кастомый queryset
    # queryset = Task.objects.filter(deleted=False)
    filters_form_class = WikiListFilters

    @csrf_exempt
    def get(self, *args, **kwargs):
        self.default_filters = {
            'tags': None,
        }
        return super(WikiList, self).get(*args, **kwargs)

    def define_filters(self):
        data = {}
        for key, default_value in self.default_filters.items():
            if key in self.request.GET:
                data[key] = self.request.GET.get(key)
            else:
                data[key] = default_value

        self.filters_form = self.filters_form_class(data)
        self.filters_values = {}
        if self.filters_form.is_valid():
            for key in self.default_filters.keys():
                self.filters_values[key] = self.filters_form.cleaned_data.get(key)

    def get_queryset(self):
        qs = WikiPage.objects.filter(level=1).order_by('level')
        # if len(self.request.GET) > 0:
        self.define_filters()

        self.queryset = qs
        return qs

    def get_context_data(self, **kwargs):
        # TODO брать из урла и переделать модуль endless_pagination, чтобы он использовал кол-во страниц из адреса или переменной вьюса.
        self.per_page = endless_settings.PER_PAGE

        context = super(WikiList, self).get_context_data(**kwargs)
        self.define_filters()

        # фильтры списка
        context['filters_form'] = self.filters_form

        context['count_objects'] = self.queryset.count()


        # def get_descendants(node):
        #     descendents = []
        #     children = node.get_children()
        #     for n in children:
        #         descendents += get_descendants(n)
        #     return [node] + descendents
        # tree = []
        # for node in WikiPage.objects.filter(level=1):
        #     tree += get_descendants(node)
        context['tree'] = WikiPage.objects.get_tree()
        return context


class AddWikiPage(CreateView):
    model = WikiPage
    template_name = 'wiki/add_wiki_page.html'
    form_class = WikiPageForm
    # fields = '__all__'

    # def get_form_kwargs(self):
    #     kwargs = super(AddWikiPage, self).get_form_kwargs()
    #     kwargs.update({
    #         'request': self.request,
    #     })
    #     return kwargs


class WikiPageDetail(DetailView):
    model = WikiPage
    template_name = 'wiki/wiki_page_detail.html'
    context_object_name = 'page'
    slug_field = 'pk'
    slug_url_kwarg = 'pk'


class WikiPageBlockDetail(DetailView):
    model = WikiPage
    template_name = 'wiki/wiki_page_detail_block.html'
    context_object_name = 'page'
    slug_field = 'pk'
    slug_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super(WikiPageBlockDetail, self).get_context_data(**kwargs)
        context.update({
            'show_title': True,
        })
        return context
