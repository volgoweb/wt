# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_auto_20150629_1223'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskStep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('completed', models.BooleanField(default=False, verbose_name='\u0421\u0434\u0435\u043b\u0430\u043d')),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('desc', models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('date', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0438\u0441\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='task_steps',
            field=models.ManyToManyField(to='task.TaskStep', verbose_name='\u0428\u0430\u0433\u0438 \u0437\u0430\u0434\u0430\u0447\u0438'),
        ),
    ]
