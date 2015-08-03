# -*- coding: utf-8 -*-
import datetime
from django.utils import timezone
from dateutil import relativedelta
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


class TaskTemplateManager(models.Manager):
    def  create_from_task(self, task):
        """
        Создание объекта шаблона из задачи.
        """
        field_values = {}
        for f in sorted(task._meta.fields):
            if f.name not in ('id','template'):
                field_values[f.name] = getattr(task, f.name)
        task_tpl = self.model(**field_values)
        task_tpl.save()
        for f in sorted(task._meta.many_to_many):
            setattr(task_tpl, f.name, getattr(task, f.name).all())
            # setattr(task_tpl, f.name, getattr(task, f.name).all())
        task_tpl.save()
        return task_tpl


class TaskTemplate(helper_models.FieldsLabelsMixin, PolymorphicModel):
    PERIOD_DAY = 'day'
    PERIOD_SOME_DAYS = 'some_days'
    PERIOD_WEEK = 'week'
    PERIOD_MONTH_BY_DAY = 'month_by_day'
    PERIOD_YEAR_BY_DAY = 'year_by_day'

    PERIOD_CHOICES = OrderedDict([
        (PERIOD_DAY, u'Каждый день'),
        # (PERIOD_SOME_DAYS, u'Каждые несколько дней'),
        (PERIOD_WEEK, u'Каждую неделю'),
        (PERIOD_MONTH_BY_DAY, u'Каждый месяц (по дню месяца)'),
        (PERIOD_YEAR_BY_DAY, u'Каждый год (по дню месяца)'),
    ])

    title = models.CharField(max_length=255, verbose_name=u'Название задачи')
    desc = models.TextField(verbose_name=u'Описание задачи', blank=True, null=True)
    performer = models.ForeignKey('account.Account', verbose_name=u'Исполнитель', related_name='%(class)s_performer')
    # должностная единица
    performer_unit = models.ForeignKey('account.CompanyUnit', verbose_name=u'Исполнитель', related_name='%(class)s_performer_unit')
    author = models.ForeignKey('account.Account', verbose_name=u'Автор', related_name='%(class)s_author')
    due_date = models.DateTimeField(null=True, blank=True, verbose_name=u'Крайний срок')
    # TODO добавить поля для клиента и партнера

    step_type = models.ForeignKey(ContentType, related_name='%(class)s_step_type', blank=True, null=True)
    step_id = models.PositiveIntegerField(blank=True, null=True)
    step = GenericForeignKey('step_type', 'step_id')

    task_steps = models.ManyToManyField('task.TaskStep', verbose_name=u'Шаги задачи', related_name='%(class)s_task_steps')
    files = models.ManyToManyField('task.TaskFile', verbose_name=u'Вложения', related_name='%(class)s_files')

    period = models.CharField(max_length=20, choices=PERIOD_CHOICES.items(), verbose_name=u'Период повторения', blank=True, null=True)
    # period_days = models.IntegerField(blank=True, null=True, verbose_name=u'Количество дней')
    # start_datetime = models.DateTimeField(verbose_name=u'Дата отсчета периода повторения')

    objects = TaskTemplateManager()

    def __unicode__(self):
        return u'#{0} {1}'.format(self.pk, self.title)

    def create_repeating_tasks(self, author=None):
        # удаляем все экземпляры повторяющихся задач, если они есть
        Task.objects.filter(template=self, is_repeating_clone=True).delete()

        dates = self.get_repeating_due_dates(start_date=self.due_date)
        task = self.task.get()
        if not author:
            author = task.author
        for d in dates:
            task = Task(
                template=self,
                due_date=d,
                author=author,
                is_repeating_clone=True,
            )
            task.save()

    def get_repeating_due_dates(self, start_date=None):
        """
        Возвращает список дат срока исполнения всех повторяющихся задач,
        начиная от указанной даты (если она не указана, то от самой начальной)
        и на 2 года в будущее (от сегодня).
        """
        now = datetime.datetime.now()
        if not start_date:
            start_date = self.due_date.date()
        delta = self.get_timedelta_period()
        end_date = now + relativedelta.relativedelta(years=10)
        dates = []
        def add_next_date(d):
            d += delta
            if d.date() < end_date.date():
                dates.append(d)
                add_next_date(d)

        add_next_date(start_date)
        return dates

    def get_timedelta_period(self):
        if self.period == self.PERIOD_DAY:
            return datetime.timedelta(days=1)
        elif self.period == self.PERIOD_WEEK:
            return datetime.timedelta(days=7)
        elif self.period == self.PERIOD_MONTH_BY_DAY:
            return relativedelta.relativedelta(months=1)
        elif self.period == self.PERIOD_YEAR_BY_DAY:
            return relativedelta.relativedelta(years=1)
        else:
            raise(u'Не удалось определить период повторения, выраженный в timedelta')



class TaskQueryset(models.query.QuerySet):
    def not_deleted(self):
        return self.filter(deleted=False)

    def in_work(self):
        return self.filter(status=self.model.STATUS_IN_WORK)

    def in_work_or_wait(self):
        return self.filter(
            status__in=(
                self.model.STATUS_IN_WORK,
                self.model.STATUS_AWATING_EXECUTION,
            ),
        )

    def performed(self, user):
        return self.filter(template__performer=user)

    def consigned(self, user, exclude_self_tasks=False):
        qs = self.filter(author=user)
        if exclude_self_tasks:
            qs = qs.exclude(template__performer=F('author'))
        return qs

    def overdue(self, *args, **kwargs):
        now = timezone.now()
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

    # def favorite(self, *args, **kwargs):
    #     return self.filter(is_favorite=True)

    def repeating(self, *args, **kwargs):
        return self.filter(is_repeating_clone=False)


class TaskManager(models.Manager):
    def get_queryset(self):
        return TaskQueryset(self.model).not_deleted()

    def create_from_template(self, tpl):
        """
        Создание из шаблона.
        """
        field_values = {}
        for f in sorted(self.model.Meta.fields):
            if f.name not in ('id',):
                field_values[f.name] = getattr(tpl, f.name)
        task = self.model(**field_values)
        task.save()
        for f in sorted(self.model.Meta.many_to_many):
            # setattr(task_tpl, f.name, getattr(task, f.name).all())
            setattr(task, f.name, getattr(tpl, f.name).all())
        task.save()
        return task


class Task(models.Model):
    STATUS_DECLINE = 'decline'
    STATUS_IN_WORK = 'in_work'
    STATUS_AWATING_EXECUTION = 'awaiting'
    STATUS_READY = 'ready'
    STATUSES = OrderedDict([
        (STATUS_DECLINE, u'Отклонена исполнителем'),
        (STATUS_AWATING_EXECUTION, u'Ожидает выполнения'),
        (STATUS_IN_WORK, u'Выполняется'),
        (STATUS_READY, u'Готова'),
    ])

    template = models.ForeignKey(
        'task.TaskTemplate',
        related_name='task',
        blank=True,
        null=True,
        verbose_name=u'Шаблон',
        help_text=u'Все базовые поля, которые могут быть использованы во всех повторяющихся экземплярах задач.',
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')
    author = models.ForeignKey('account.Account', verbose_name=u'Автор', related_name='%(class)s_author')
    due_date = models.DateTimeField(null=True, blank=True, verbose_name=u'Крайний срок')
    status = models.CharField(max_length=20, choices=STATUSES.items(), default=STATUS_IN_WORK, verbose_name=u'Статус задачи')
    # is_favorite = models.BooleanField(default=False, verbose_name=u'Избранная')
    deleted = models.BooleanField(default=False, verbose_name=u'Удаленная')
    is_repeating_clone = models.BooleanField(default=False, verbose_name=u'Клон повторяющейся задачи')

    objects = TaskManager()

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return u'#{0}'.format(self.pk)

    def get_absolute_url(self):
        return reverse('task:task_detail', kwargs={'pk':self.pk})

    def get_results(self):
        # """
        # Возвращает список заголовков и значений полей, отвечающих за результат выполнения.
        # Такие поля как 'комментарий', 'статус' и поля из дочерних классов.
        # """
        values = []
        for obj in (self, self.template):
            fields = obj._meta.fields
            for f in fields:
                if f.name not in ('id', 'polymorphic_ctype', 'step_id', 'step_type', 'template', 'performer', 'is_repeating_clone', 'deleted'):
                    getting_human_value_method = getattr(obj, 'get_{0}_display'.format(f.name), None)
                    if callable(getting_human_value_method):
                        val = getting_human_value_method()
                    else:
                        val = getattr(obj, f.name)
                    if f.name == 'performer_unit':
                        # TODO вынести в какой-то общий метод или helper функцию
                        val = u'{0} ({1})'.format(val.get_user(), val.name)
                    values.append({
                        'label': f.verbose_name,
                        'value': val or '',
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

    def is_overdue(self):
        if self.due_date and self.status not in (self.STATUS_DECLINE, self.STATUS_READY):
            now = timezone.now()
            if self.due_date < now:
                return True
        return False

    def save(self, *args, **kwargs):
        super(Task, self).save(*args, **kwargs)
        if self.status in (self.STATUS_READY, self.STATUS_DECLINE):
            if self.step:
                self.step.end(task=self, request=self.request)


class RepeatParamsManager(models.Manager):
    def create_next_task(self, task):
        task.template
        next_task = Task.objects.create_from_template(task.template)
        next_task.due_date = task.template.repeat_params.get_next_due_date(task.due_date)
        next_task.template = task.template
        next_task.save()


# @receiver(post_save, sender=Task)
# def post_save_task(instance, **kwargs):
#     # TODO перенести в ассинхронное выполнение через celery
#     task = instance
#     created = kwargs.get('created')
#     # TODO сделать проверку изменились ли параметры повторения или нет
#     if hasattr(task.template, 'repeat_params') and not task.is_repeating_clone:
#         task.template.create_repeating_tasks()

@receiver(post_save, sender=Task)
def post_save_task(instance, **kwargs):
    task = instance
    template = task.template
    if template.period and not task.is_repeating_clone:
        template.create_repeating_tasks()

@receiver(post_save, sender=TaskTemplate)
def post_save_task_template(instance, created, **kwargs):
    if created:
        task = Task(
            template=instance,
            due_date=instance.due_date,
            author=instance.author,
        )
        task.save()
