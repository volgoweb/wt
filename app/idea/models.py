# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse_lazy


class IdeaQueryset(models.query.QuerySet):
    def not_deleted(self):
        return self.filter(deleted=False)


class IdeaManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return IdeaQueryset(self.model)


class Idea(models.Model):
    title = models.CharField(max_length=254, verbose_name=u'Заголовок')
    desc = models.TextField(max_length=15000, verbose_name=u'Описание', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')
    edited = models.DateTimeField(auto_now=True, editable=False, verbose_name=u'Дата изменения')
    author = models.ForeignKey('account.Account', verbose_name=u'Автор', related_name='idea_of_author')
    # destination_unit = models.ForeignKey('account.CompanyUnit', verbose_name=u'Предназначено для', related_name='idea_of_destination')
    deleted = models.BooleanField(default=False, verbose_name=u'Удаленная')

    objects = IdeaManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('idea:idea_detail_page', kwargs={'pk': self.pk})
