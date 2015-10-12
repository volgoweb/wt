# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from polymorphic import PolymorphicModel
from django.db.models.signals import post_save, pre_save
import django.dispatch
from django.core.mail import send_mail
from django_comments.signals import comment_was_posted

from app.task.models import Task
from app.task.signals import task_saved
from app.crm.models import SalesDeal


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


@receiver(task_saved, sender=Task)
def notify_about_task(task, created, **kwargs):
    # TODO перенести в ассинхронное выполнение через celery
    if created and task.author != task.template.performer:
        text = u'Добавлена новая задача "<a href="{link}">{title}</a>"'.format(link=task.get_absolute_url(), title=task.template.title)
        n = Notification(
            text=text,
            subscriber=task.template.performer,
            obj=task,
        )
        n.save()

        try:
            send_mail(u'Добавлена новая задача', text, 'dima_page@mail.ru', [task.template.performer.email], fail_silently=False)
        except:
            pass

# task_saved.connect(notify_about_task)

@receiver(comment_was_posted)
def notify_about_adding_comment(*args, **kwargs):
    comment = kwargs.get('comment')
    obj = comment.content_object
    subscribers = []
    if type(obj) == Task:
        task = obj
        subscribers.append(obj.author)
        if obj.template.performer != obj.author:
            subscribers.append(obj.template.performer)
        for u in subscribers:
            text = u'Добавлен комментарий к задаче "<a href="{link}">{title}</a>": <span class="notify-item__comment">"{comment}"</span>'.format(link=task.get_absolute_url(), title=task.template.title, comment=comment.comment)
            n = Notification(
                text=text,
                subscriber=u,
                obj=comment,
            )
            n.save()

        try:
            send_mail(u'Добавлен комментарий', text, 'dima_page@mail.ru', [u.email for u in subscribers], fail_silently=False)
        except:
            pass


@receiver(post_save, sender=SalesDeal)
def notify_about_sales_deal(sender, instance, *args, **kwargs):
    # TODO перенести в ассинхронное выполнение через celery
    subscriber_emails = [instance.responsible]
    if kwargs.get('created'):
        subject = u'Добавлена новая сделка'
        text = u'Добавлена новая сделка "<a href="{link}">{title}</a>"'.format(link=instance.get_absolute_url(), title=instance.title)
    else:
        subject = u'Изменена сделка'
        text = u'Изменена сделка "<a href="{link}">{title}</a>"'.format(link=instance.get_absolute_url(), title=instance.title)
    n = Notification(
        text=text,
        subscriber=instance.responsible,
        obj=instance,
    )
    n.save()

    try:
        send_mail(subject, text, 'dima_page@mail.ru', [subscriber_emails], fail_silently=False)
    except:
        pass
