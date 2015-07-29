# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_remove_task_is_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='template',
            field=models.ForeignKey(related_name='task', blank=True, to='task.TaskTemplate', help_text='\u0412\u0441\u0435 \u0431\u0430\u0437\u043e\u0432\u044b\u0435 \u043f\u043e\u043b\u044f, \u043a\u043e\u0442\u043e\u0440\u044b\u0435 \u043c\u043e\u0433\u0443\u0442 \u0431\u044b\u0442\u044c \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u044b \u0432\u043e \u0432\u0441\u0435\u0445 \u043f\u043e\u0432\u0442\u043e\u0440\u044f\u044e\u0449\u0438\u0445\u0441\u044f \u044d\u043a\u0437\u0435\u043c\u043f\u043b\u044f\u0440\u0430\u0445 \u0437\u0430\u0434\u0430\u0447.', null=True, verbose_name='\u0428\u0430\u0431\u043b\u043e\u043d'),
        ),
    ]
