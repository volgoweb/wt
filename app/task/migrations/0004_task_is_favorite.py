# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_auto_20150705_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='is_favorite',
            field=models.BooleanField(default=False, verbose_name='\u0418\u0437\u0431\u0440\u0430\u043d\u043d\u0430\u044f'),
        ),
    ]
