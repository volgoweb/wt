# -*- coding: utf-8 -*-
"""
Маршрут для форумки.
Контент-менеджер создает инфоповод.
Автор пишет по инфоповоду заголовок и текст.
Контент-менеджер подбирает картинки.
Корректор проверяет и исправляет ошибки.
Контент-менеджер публикует.
"""
import json
import datetime
from django.db import models
from django.core.urlresolvers import reverse

from app.route.models import BaseRoute, BaseStep
from app.task.models import (
    Task
)
# TODO вынести одинаковый функционал в отдельные методы


class Step1(BaseStep):
    class Meta:
        proxy = True

    def run(self, **kwargs):
        super(Step1, self).run(**kwargs)
        task = Task(
            title=u'Поиск товара и информирование клиента о сроках отгрузки.',
            desc=u"""Проверьте наличие каждого заказанного товара и сообщите клиенту: 1) какие товары есть в наличии; 2) цену каждого товара; 3) срок поставки товаров, которых нет в наличие 4) альтернативу тем товарам, которых нет в наличие. \n Описание заявки клиента: {0}""".format(kwargs['application_desc']),
            performer=kwargs['manager'],
            step=self,
        )
        task.save()

        self.task = task
        self.save()

    def end(self, **kwargs):
        super(Step1, self).end(**kwargs)

        next_step = self.route.get_step(name=Route.STEP_CREATE_ORDER)
        next_step.run()


class Step2(BaseStep):
    class Meta:
        proxy = True

    def run(self, **kwargs):
        super(Step2, self).run(**kwargs)
        task = Task(
            title=u'Формирование заказа в 1С',
            desc=u'Сформируйте заказ на отгрузку товара, который в наличие.',
            performer=self.route.manager,
            step=self,
        )
        task.save()

        task = Task(
            title=u'Заказать у поставщиков товар, которого нет в наличие',
            desc=u'Сформируйте заказ на отгрузку товара, который в наличие.',
            performer=self.route.manager,
            step=self,
        )
        task.save()

    def end(self, **kwargs):
        super(Step2, self).end(**kwargs)

        next_step = self.route.get_step(name=Route.STEP_CREATE_ORDER)
        next_step.run()
        self.save()


class Route(BaseRoute):
    STEP_FIRST = 'first'
    STEP_CREATE_ORDER = 'create_order'

    application_desc = models.CharField(max_length=20000, blank=True, null=True)
    manager = models.ForeignKey('account.Account', blank=True, null=True)

    # class Meta:
    #     proxy = True

    def save(self, *args, **kwargs):
        is_new = False if self.pk else True
        super(Route, self).save(*args, **kwargs)

        if is_new:
            s1 = Step1(
                name=self.STEP_FIRST,
                route=self,
            )
            s1.save()

            s2 = Step2(
                name=self.STEP_CREATE_ORDER,
                route=self,
            )
            s2.save()

            # s3 = Step3(
            #     name=self.STEP_CHECK_BY_CORRECTOR,
            #     route=self,
            # )
            # s3.save()

            # s4 = Step4(
            #     name=self.STEP_GIVE_IMAGES,
            #     route=self,
            # )
            # s4.save()

            # s5 = Step5(
            #     name=self.STEP_PUBLISH,
            #     route=self,
            # )
            # s5.save()

    def run(self):
        self.article = Article()
        self.article.save()

        step = self.steps.get(name='S1')
        step.run()
