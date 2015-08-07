# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Count

from helper.models import Dictionary
from app.task.models import Task
from app.task.signals import task_saved

class DealStatus(Dictionary):
    pass


class SalesDealQueryset(models.query.QuerySet):
    def with_responsible(self, user):
        return self.filter(responsible_unit=user.job)


class SalesDealManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return SalesDealQueryset(self.model).all()

    def count_of_responisble_by_status(self, user):
        qs = self.get_queryset().with_responsible(user)
        values = qs.values('status').annotate(count_rows=Count('status'))
        counts = {}
        for v in values:
            counts[v.get('status')] = v.get('count_rows')
        return counts


class SalesDeal(models.Model):
    title = models.CharField(max_length=255, verbose_name=u'Название')
    desc = models.TextField(verbose_name=u'Описание', blank=True, null=True)
    client_company = models.ForeignKey('contact.Company', related_name='sales_deal', verbose_name=u'Компания клиента')
    client_contact = models.ForeignKey('contact.Contact', related_name='sales_deal', verbose_name=u'Контактное лицо клиента')
    responsible_unit = models.ForeignKey('account.CompanyUnit', related_name='sales_deal', verbose_name=u'Ответственный')
    responsible = models.ForeignKey('account.Account', related_name='sales_deal', verbose_name=u'Ответственный (аккаунт)')
    budget = models.IntegerField(blank=True, null=True, verbose_name=u'Бюджет')
    status = models.ForeignKey('crm.DealStatus', related_name='sales_deal', verbose_name=u'Статус')
    tasks = models.ManyToManyField('task.Task', related_name='sales_deal', verbose_name=u'Задачи')
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')
    edited = models.DateTimeField(auto_now=True, editable=False, verbose_name=u'Дата изменения')
    author = models.ForeignKey('account.Account', verbose_name=u'Автор', related_name='sales_deal_of_author')
    deleted = models.BooleanField(default=False, verbose_name=u'Удаленная')

    objects = SalesDealManager()

    def get_next_task(self):
        tasks = self.tasks.filter(status__in=Task.OPENED_STATUSES).order_by('due_date')
        if tasks:
            return tasks[0]

    def is_open(self, *args, **kwargs):
        if getattr(self.status, 'pk', None) != 'closed':
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        if self.responsible_unit:
            user = self.responsible_unit.get_user()
            self.responsible = user
        return super(SalesDeal, self).save(*args, **kwargs)


def task_saved_handler(task, created, request, **kwargs):
    if created:
        deal_pk = request.GET.get('sales_deal', None)
        if deal_pk:
            try:
                deal = SalesDeal.objects.get(pk=deal_pk)
                deal.tasks.add(task)
                deal.save()
            except:
                pass
task_saved.connect(task_saved_handler)
