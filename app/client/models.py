# -*- coding: utf-8 -*-
from django.db import models


class ClientQueryset(models.db.QuerySet):
    def not_deleted(self):
        return self.filter(deleted=False)


class ClientManager(models.Manager):
    def get_queryset(self):
        return ClientQueryset(self.model).not_deleted()


class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'Название')
    desc = models.TextField(verbose_name=u'Описание', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')
    author = models.ForeignKey('account.Account', verbose_name=u'Автор')
    # files = models.ManyToManyField('task.TaskFile', verbose_name=u'Вложения')
    # is_favorite = models.BooleanField(default=False, verbose_name=u'Избранная')
    deleted = models.BooleanField(default=False, verbose_name=u'Удаленный')
    # TODO добавить теги

    objects = ClientManager()