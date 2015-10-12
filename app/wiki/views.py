# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, UpdateView
from endless_pagination.views import AjaxListView
from endless_pagination import settings as endless_settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

from .models import WikiPage
from .forms import WikiListFilters, WikiPageForm
from .signals import wiki_page_saved

class WikiList(AjaxListView):
    model = WikiPage
    template_name = 'wiki/wiki_list_page.html'
    page_template = template_name
    context_object_name = 'tree'
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
        pages = WikiPage.objects.get_tree(perm=WikiPage.PERM_VIEW, user=self.request.user)
        if self.kwargs.get('list_name') == 'my':
            pages = filter(lambda p: p.performers.filter(pk=self.request.user.pk).exists(), pages)
        return pages

    def get_context_data(self, **kwargs):
        # TODO брать из урла и переделать модуль endless_pagination, чтобы он использовал кол-во страниц из адреса или переменной вьюса.
        self.per_page = endless_settings.PER_PAGE

        context = super(WikiList, self).get_context_data(**kwargs)
        self.define_filters()

        # фильтры списка
        context['filters_form'] = self.filters_form

        context['count_objects'] = len(context['tree'])
        return context


class AddWikiPage(CreateView):
    model = WikiPage
    template_name = 'wiki/add_wiki_page.html'
    form_class = WikiPageForm
    # fields = '__all__'

    def get_form_kwargs(self):
        kwargs = super(AddWikiPage, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def form_valid(self, form, *args, **kwargs):
        wiki_page = form.save()
        wiki_page_saved.send(sender=WikiPage, wiki_page=wiki_page, created=True, request=self.request)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('wiki:wiki_list_page', kwargs={'list_name': 'my'})


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
        obj = self.get_object()
        context['can_edit'] = obj.has_user_perm_in_wiki_page(user=self.request.user, perm=obj.PERM_EDIT)
        return context


class WikiPageDetail(WikiPageBlockDetail):
    template_name = 'wiki/wiki_page_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(WikiPageDetail, self).get_context_data(**kwargs)
        context.update({
            'show_title': False,
        })
        return context


class EditWikiPage(UpdateView):
    model = WikiPage
    template_name = 'wiki/edit_wiki_page.html'
    form_class = WikiPageForm
    context_object_name = 'page'

    def get_form_kwargs(self):
        kwargs = super(EditWikiPage, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def form_valid(self, form, *args, **kwargs):
        wiki_page = form.save()
        wiki_page_saved.send(sender=WikiPage, wiki_page=wiki_page, created=False, request=self.request)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('wiki:wiki_list_page', kwargs={'list_name': 'my'})
