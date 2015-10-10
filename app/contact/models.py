# -*- coding: utf-8 -*-
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'Название')
    desc = models.TextField(verbose_name=u'Описание', blank=True, null=True, help_text="Общее описание, режим работы, общие контакты и адреса офисов.")
    is_lead = models.BooleanField(default=False, verbose_name=u'Потенциальный клиент')
    is_client = models.BooleanField(default=False, verbose_name=u'Клиент')
    is_partner = models.BooleanField(default=False, verbose_name=u'Партнер')
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания')
    changed = models.DateTimeField(auto_now=True, editable=False, verbose_name=u'Дата изменения')
    author = models.ForeignKey('account.Account', verbose_name=u'Автор')
    deleted = models.BooleanField(default=False, verbose_name=u'Удаленный')

    def __unicode__(self, *args, **kwargs):
        return self.name


class Contact(models.Model):
    full_name = models.CharField(max_length=255, verbose_name=u'Полное имя')
    desc = models.TextField(verbose_name=u'Описание', blank=True, null=True)
    company = models.ForeignKey(Company, verbose_name=u'Компания', blank=True, null=True)
    phone = models.CharField(max_length=30, verbose_name=u'Телефон', blank=True, null=True)
    mobile_phone = models.CharField(max_length=30, verbose_name=u'Мобильный тел.', blank=True, null=True)
    email = models.EmailField(max_length=200, verbose_name=u'Email', blank=True, null=True)
    is_lead = models.BooleanField(default=False, verbose_name=u'Потенциальный клиент')
    is_client = models.BooleanField(default=False, verbose_name=u'Клиент')
    is_partner = models.BooleanField(default=False, verbose_name=u'Партнер')
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания')
    changed = models.DateTimeField(auto_now=True, editable=False, verbose_name=u'Дата изменения')
    author = models.ForeignKey('account.Account', verbose_name=u'Автор')
    deleted = models.BooleanField(default=False, verbose_name=u'Удаленный')
    # TODO добавить флаг избранности (для каждого сотрудника отдельно)
    # TODO добавить теги

    def __unicode__(self, *args, **kwargs):
        return self.full_name
