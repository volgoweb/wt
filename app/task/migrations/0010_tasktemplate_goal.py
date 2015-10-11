# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goal', '0003_auto_20150807_1452'),
        ('task', '0009_tasktemplate_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasktemplate',
            name='goal',
            field=models.ForeignKey(verbose_name='\u0426\u0435\u043b\u044c', blank=True, to='goal.Goal', null=True),
        ),
    ]
