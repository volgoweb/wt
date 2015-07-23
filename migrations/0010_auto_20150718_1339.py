# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0009_auto_20150716_0453'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepeatParams',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('period', models.CharField(max_length=20, verbose_name='\u041f\u0435\u0440\u0438\u043e\u0434 \u043f\u043e\u0432\u0442\u043e\u0440\u0435\u043d\u0438\u044f', choices=[(b'day', '\u041a\u0430\u0436\u0434\u044b\u0439 \u0434\u0435\u043d\u044c'), (b'week', '\u041a\u0430\u0436\u0434\u0443\u044e \u043d\u0435\u0434\u0435\u043b\u044e'), (b'month_by_day', '\u041a\u0430\u0436\u0434\u044b\u0439 \u043c\u0435\u0441\u044f\u0446 (\u043f\u043e \u0434\u043d\u044e \u043c\u0435\u0441\u044f\u0446\u0430)'), (b'year_by_day', '\u041a\u0430\u0436\u0434\u044b\u0439 \u0433\u043e\u0434 (\u043f\u043e \u0434\u043d\u044e \u043c\u0435\u0441\u044f\u0446\u0430)')])),
            ],
        ),
        migrations.CreateModel(
            name='TaskTemplate',
            fields=[
                ('task_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='task.Task')),
                ('repeat_params', models.ForeignKey(related_name='repeat_params', verbose_name='\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u043f\u043e\u0432\u0442\u043e\u0440\u0435\u043d\u0438\u044f', blank=True, to='task.RepeatParams', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('task.task',),
        ),
        migrations.RemoveField(
            model_name='periodictask',
            name='task_ptr',
        ),
        migrations.RemoveField(
            model_name='task',
            name='periodic_task',
        ),
        migrations.DeleteModel(
            name='PeriodicTask',
        ),
        migrations.AddField(
            model_name='task',
            name='template',
            field=models.ForeignKey(related_name='template_in_task', verbose_name='\u0428\u0430\u0431\u043b\u043e\u043d', blank=True, to='task.TaskTemplate', null=True),
        ),
    ]
