# -*- coding: utf-8 -*-
from django.db import models

from helper.models import Dictionary

class DealStatus(Dictionary):
    pass

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

    def save(self, *args, **kwargs):
        if self.responsible_unit:
            user = self.responsible_unit.get_user()
            self.responsible = user
        return super(SalesDeal, self).save(*args, **kwargs)
