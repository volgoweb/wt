# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_auto_20150729_0322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasktemplate',
            name='repeat_params',
            field=models.ForeignKey(related_name='template', verbose_name='\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u043f\u043e\u0432\u0442\u043e\u0440\u0435\u043d\u0438\u044f', blank=True, to='task.RepeatParams', null=True),
        ),
    ]
