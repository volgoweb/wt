# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_task_is_favorite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='files',
        ),
    ]
