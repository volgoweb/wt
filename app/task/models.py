# -*- coding: utf-8 -*-
import datetime
from collections import OrderedDict
from django.db import models
from django.db.models import F
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from polymorphic import PolymorphicModel
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from helper import models as helper_models
from .signals import task_saved

# TODO добавить миксины для разных повторяющихся полей

# TODO ??? может быть стоит добавить задачам автора
# и авторам дать возможность редактировать исполнителя задачи и статус.

# TODO Чтобы давать возможность менять автора текста на произвольном этапе, можно:
# - например, в форме инфоповода выводить список кнопок-действий.
#   Список и параметры этих кнопок задает маршрут.
#   Следовательно, инфоповод единообразен и запрашивает список кнопок
#   у своего маршрута.
# - Может быть в задачах выводить список возможных действий,
#   который берется из шага, к которому относится задача.


class TaskFile(models.Model):
    """
    Пытался сделать общую модель для хранения файлов,
    но так и не смог отладить работу с formset этой модели.
    Поэтому костыльно делаю отдельную модель для файлов задачи.
    """
    # task = models.ForeignKey('task.Task')
    file = models.FileField(
        upload_to = 'files',
        verbose_name = u'Файл',
    )


class TaskStep(models.Model):
    completed = models.BooleanField(default=False, verbose_name=u'Сделан')
    title = models.CharField(max_length=255, verbose_name=u'Название')
    desc = models.TextField(blank=True, null=True, verbose_name=u'Описание')
    date = models.DateTimeField(blank=True, null=True, verbose_name=u'Дата исполнения')


class TaskQueryset(models.query.QuerySet):
    def not_deleted(self):
        return self.filter(deleted=False)

    def in_work(self):
        return self.filter(status=self.model.STATUS_IN_WORK)

    def performed(self, user):
        return self.filter(performer=user)

    def consigned(self, user, exclude_self_tasks=False):
        qs = self.filter(author=user)
        if exclude_self_tasks:
            qs = qs.exclude(performer=F('author'))
        return qs

    def overdue(self, *args, **kwargs):
        now = datetime.datetime.now()
        return self.filter(due_date__lt=now)

    def today(self, *args, **kwargs):
        today = datetime.date.today()
        start_of_today = datetime.datetime(today.year, today.month, today.day, 00, 00, 01)
        end_of_today = datetime.datetime(today.year, today.month, today.day, 23, 59, 59)
        return self.filter(
            due_date__range=(start_of_today, end_of_today),
        )

    def later_than_today_or_without_due(self, *args, **kwargs):
        today = datetime.date.today()
        end_of_today = datetime.datetime(today.year, today.month, today.day, 23, 59, 59)
        return self.filter(
            models.Q(due_date__gt=end_of_today) |
            models.Q(due_date__isnull=True)
        )

    def completed(self, *args, **kwargs):
        return self.filter(status=self.model.STATUS_READY)

    def favorite(self, *args, **kwargs):
        return self.filter(is_favorite=True)


class TaskManager(models.Manager):
    def get_queryset(self):
        return TaskQueryset(self.model).not_deleted()


class Task(helper_models.FieldsLabelsMixin, PolymorphicModel):
    STATUS_DECLINE = 'decline'
    STATUS_IN_WORK = 'in_work'
    STATUS_READY = 'ready'
    STATUSES = OrderedDict([
        (STATUS_DECLINE, u'Отклонена'),
        (STATUS_IN_WORK, u'В работе'),
        (STATUS_READY, u'Готова'),
    ])

    title = models.CharField(max_length=255, verbose_name=u'Название задачи')
    desc = models.TextField(verbose_name=u'Описание задачи', blank=True, null=True)
    performer = models.ForeignKey('account.Account', verbose_name=u'Исполнитель', related_name="task_performer")
    due_date = models.DateTimeField(null=True, blank=True, verbose_name=u'Крайний срок')
    comments = models.ManyToManyField('comment.Comment', verbose_name=u'Комментарий')

    step_type = models.ForeignKey(ContentType, related_name='step_type', blank=True, null=True)
    step_id = models.PositiveIntegerField(blank=True, null=True)
    step = GenericForeignKey('step_type', 'step_id')

    status = models.CharField(max_length=20, choices=STATUSES.items(), default=STATUS_IN_WORK, verbose_name=u'Статус задачи')
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')
    author = models.ForeignKey('account.Account', verbose_name=u'Автор')
    files = models.ManyToManyField('task.TaskFile', verbose_name=u'Вложения')
    is_favorite = models.BooleanField(default=False, verbose_name=u'Избранная')
    deleted = models.BooleanField(default=False, verbose_name=u'Удаленная')

    task_steps = models.ManyToManyField('task.TaskStep', verbose_name=u'Шаги задачи')

    periodic_task = models.ForeignKey('task.PeriodicTask', related_name='periodic_task_in_task', verbose_name=u'Периодическая задача', blank=True, null=True)

    objects = TaskManager()

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        return reverse('task:task_detail', kwargs={'pk':self.pk})

    def get_results(self):
        # """
        # Возвращает список заголовков и значений полей, отвечающих за результат выполнения.
        # Такие поля как 'комментарий', 'статус' и поля из дочерних классов.
        # """
        fields = self._meta.fields
        values = []
        for f in fields:
            if f.name not in ('id', 'polymorphic_ctype', 'title', 'desc', 'step_id', 'step_type', 'task_ptr'):
                getting_human_value_method = getattr(self, 'get_{0}_display'.format(f.name), None)
                if callable(getting_human_value_method):
                    val = getting_human_value_method()
                else:
                    val = getattr(self, f.name)
                values.append({
                    'label': f.verbose_name,
                    'value': val,
                })
        return values

    def is_new(self):
        """
        Возвращает True, если задача новая.
        """
        if self.status == self.STATUS_IN_WORK:
            return True
        return False

    def is_ready(self):
        """
        Возвращает True, если задача завершена.
        """
        if self.status in (self.STATUS_READY, self.STATUS_DECLINE):
            return True
        return False

    def save(self, *args, **kwargs):
        super(Task, self).save(*args, **kwargs)
        if self.status in (self.STATUS_READY, self.STATUS_DECLINE):
            if self.step:
                self.step.end(task=self, request=self.request)

        task_saved.send(sender=self.__class__, task=self)


class PeriodicTaskManager(models.Manager):
    def create_next_task(self, task):
        pass


class PeriodicTask(Task):
    PERIOD_DAY = 'day'
    PERIOD_SOME_DAYS = 'some_days'
    PERIOD_WEEK = 'week'
    PERIOD_MONTH_BY_DAY = 'month_by_day'
    PERIOD_YEAR_BY_DAY = 'year_by_day'

    PERIOD_CHOICES = OrderedDict([
        (PERIOD_DAY, u'Каждый день'),
        (PERIOD_SOME_DAYS, u'Каждые несколько дней'),
        (PERIOD_WEEK, u'Каждую неделю'),
        (PERIOD_MONTH_BY_DAY, u'Каждый месяц (по дню месяца)'),
        (PERIOD_YEAR_BY_DAY, u'Каждый год (по дню месяца)'),
    ])

    period = models.CharField(max_length=20, choices=PERIOD_CHOICES.items(), verbose_name=u'Период повторения')
    period_days = models.IntegerField(blank=True, null=True, verbose_name=u'Количество дней')

    objects = PeriodicTaskManager()


@receiver(post_save, sender=Task)
def post_save_task(**kwargs):
    # TODO перенести в ассинхронное выполнение через celery
    task = kwargs['instance']
    if task.periodic_task and task.status in (task.STATUS_READY, task.STATUS_DECLINE):
        PeriodicTask.objects.create_next_task(task)
