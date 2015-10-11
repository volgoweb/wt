# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

class GoalQueryset(models.query.QuerySet):
    def not_overdue(self):
        now = timezone.now()
        return self.filter(date_to__gte=now.date())

    def not_deleted(self):
        return self.filter(deleted=False)


class GoalManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return GoalQueryset(self.model)


class Goal(models.Model):
    title = models.CharField(max_length=254, verbose_name=u'Заголовок')
    desc = models.TextField(max_length=15000, verbose_name=u'Описание', null=True, blank=True)
    date_from = models.DateField(blank=True, null=True, verbose_name=u'Дата начала')
    date_to = models.DateField(blank=True, null=True, verbose_name=u'Дата окончания')
    performers = models.ManyToManyField('account.CompanyUnit', verbose_name=u'Исполнители', blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')
    edited = models.DateTimeField(auto_now=True, editable=False, verbose_name=u'Дата изменения')
    author = models.ForeignKey('account.Account', verbose_name=u'Автор', related_name='goal_of_author')
    deleted = models.BooleanField(default=False, verbose_name=u'Удаленная')

    objects = GoalManager()

    def __unicode__(self):
        return self.title
