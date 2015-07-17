# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0007_auto_20150713_0139'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeriodicTask',
            fields=[
                ('task_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='task.Task')),
                ('period', models.CharField(max_length=20, verbose_name='\u041f\u0435\u0440\u0438\u043e\u0434 \u043f\u043e\u0432\u0442\u043e\u0440\u0435\u043d\u0438\u044f', choices=[(b'day', '\u041a\u0430\u0436\u0434\u044b\u0439 \u0434\u0435\u043d\u044c'), (b'some_days', '\u041a\u0430\u0436\u0434\u044b\u0435 \u043d\u0435\u0441\u043a\u043e\u043b\u044c\u043a\u043e \u0434\u043d\u0435\u0439'), (b'week', '\u041a\u0430\u0436\u0434\u0443\u044e \u043d\u0435\u0434\u0435\u043b\u044e'), (b'month_by_day', '\u041a\u0430\u0436\u0434\u044b\u0439 \u043c\u0435\u0441\u044f\u0446 (\u043f\u043e \u0434\u043d\u044e \u043c\u0435\u0441\u044f\u0446\u0430)'), (b'year_by_day', '\u041a\u0430\u0436\u0434\u044b\u0439 \u0433\u043e\u0434 (\u043f\u043e \u0434\u043d\u044e \u043c\u0435\u0441\u044f\u0446\u0430)')])),
                ('period_days', models.IntegerField(null=True, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0434\u043d\u0435\u0439', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('task.task',),
        ),
        migrations.AddField(
            model_name='task',
            name='periodic_task',
            field=models.ForeignKey(related_name='periodic_task_in_task', verbose_name='\u041f\u0435\u0440\u0438\u043e\u0434\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430', blank=True, to='task.PeriodicTask', null=True),
        ),
    ]
