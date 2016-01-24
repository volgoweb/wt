# -*- coding: utf-8 -*-
from django.db import models
from collections import OrderedDict
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from polymorphic.models import PolymorphicModel

from app.task.models import Task


class BaseStep(PolymorphicModel):
    STATUS_NOT_RUN = 'not_run'
    STATUS_IN_WORK = 'in_work'
    STATUS_READY = 'ready'

    STATUSES = OrderedDict([
        (STATUS_NOT_RUN, STATUS_NOT_RUN),
        (STATUS_IN_WORK, STATUS_IN_WORK),
        (STATUS_READY, STATUS_READY),
    ])

    # TODO скорее всего надо удалить
    name = models.CharField(max_length=255)
    # Сериализованные результаты выполнения шага
    # TODO создать тип поля, которое будет автоматически сериализовать/десериализовать
    results = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUSES.items(), default=STATUS_NOT_RUN)

    task_type = models.ForeignKey(ContentType, related_name='task_type', blank=True, null=True)
    task_id = models.PositiveIntegerField(blank=True, null=True)
    task = GenericForeignKey('task_type', 'task_id')

    route_type = models.ForeignKey(ContentType, related_name='route_type', blank=True, null=True)
    route_id = models.PositiveIntegerField()
    route = GenericForeignKey('route_type', 'route_id')

    def __unicode__(self):
        return u'id:{0} {1} (route_id:{2})'.format(self.pk, self.name, self.route_id)

    def run(self, **kwargs):
        self.status = self.STATUS_IN_WORK
        self.save()

    def end(self, **kwargs):
        self.status = self.STATUS_READY
        self.save()

    def create_inforeason_and_article(self, **kwargs):
        """
        Создание инфоповода.
        """
        self.create_article()

        ir = Inforeason(
            title=kwargs.get('title', None),
            desc=kwargs.get('desc', None),
            source_link=kwargs.get('source_link', None),
            project=kwargs.get('project', None),
            article=self.route.article,
            plan_publicating_date=kwargs.get('plan_publicating_date'),
        )
        ir.save()

        self.route.inforeason = ir
        self.route.save()

    def create_article(self):
        """
        Создание статьи.
        """
        article = Article()
        article.save()
        self.route.article = article

    def remove_step_tasks(self):
        """
        Деактивирует все задачи по данному шагу.
        """
        Task.objects.filter(step_id=self.pk, deleted=False).update(deleted=True)

    def get_actions(self, **kwargs):
        """
        Возвращает список действий, доступных на данном шаге
        (может учитываться авторизованный пользователь).
        Переопределяется в дочерних классах.
        """
        return []

    def run_action(self, action_name, action_kwargs={}):
        """
        Запускает указанное действие шага.
        """
        action = getattr(self, 'run_%s_action' % action_name, None)
        if callable(action):
            action(**action_kwargs)


class BaseRoute(PolymorphicModel):
    def __unicode__(self):
        return u'id:{0} ir:{2}'.format(self.pk, self.inforeason.pk)

    def get_step(self, name):
        steps = BaseStep.objects.filter(route_id=self.pk, name=name)
        return BaseStep.objects.get(route_id=self.pk, name=name)

