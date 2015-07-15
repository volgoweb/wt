# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0004_auto_20150715_0547'),
    ]

    operations = [
        migrations.AddField(
            model_name='wikipage',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='\u0423\u0434\u0430\u043b\u0435\u043d\u043d\u0430\u044f'),
        ),
    ]
