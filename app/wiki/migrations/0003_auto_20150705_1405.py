# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0002_auto_20150701_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wikipage',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='children', verbose_name='\u0420\u043e\u0434\u0438\u0442\u0435\u043b\u044c\u0441\u043a\u0430\u044f \u0433\u043b\u0430\u0432\u0430', blank=True, to='wiki.WikiPage', null=True),
        ),
    ]
