# -*- coding: utf-8 -*-
from django.db import models

class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')
    author = models.ForeignKey('account.Account', verbose_name=u'Автор')
    text = models.TextField(max_length=5000)
    files = models.ManyToManyField('core.FileItem', verbose_name=u'Вложения')
    deleted = models.BooleanField(default=False, verbose_name=u'Удаленная')
