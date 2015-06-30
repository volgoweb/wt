# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from polymorphic import PolymorphicModel
from django.db.models.signals import post_save, pre_save
import django.dispatch
from django.core.mail import send_mail

from app.task.models import Task
from app.task.signals import task_saved


class Notification(PolymorphicModel):
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата события')
    readed = models.BooleanField(default=False, verbose_name=u'Прочитано')
    text = models.TextField(verbose_name=u'Описание события')
    subscriber = models.ForeignKey('account.Account', verbose_name=u'Подписчик')

    obj_type = models.ForeignKey(ContentType, related_name='obj_type', blank=True, null=True)
    obj_id = models.PositiveIntegerField(blank=True, null=True)
    obj = GenericForeignKey('obj_type', 'obj_id')

    class Meta:
        ordering = ('-created',)


# @receiver(task_saved, sender=Task)
def notify_about_task(**kwargs):
    # TODO перенести в ассинхронное выполнение через celery
    task = kwargs.get('task')
    if task.is_new():
        text = u'Добавлена новая задача "<a href="{link}">{title}</a>"'.format(link=task.get_absolute_url(), title=task.title)
        n = Notification(
            text=text,
            subscriber=task.performer,
            obj=task,
        )
        n.save()

        try:
            send_mail(u'Добавлена новая задача', text, 'dima_page@mail.ru', [task.performer.email], fail_silently=False)
        except:
            pass

task_saved.connect(notify_about_task)
