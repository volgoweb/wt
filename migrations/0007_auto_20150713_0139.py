# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0006_auto_20150713_0129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='files',
            field=models.ManyToManyField(to='task.TaskFile', verbose_name='\u0412\u043b\u043e\u0436\u0435\u043d\u0438\u044f'),
        ),
    ]
