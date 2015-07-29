# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_auto_20150723_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='repeatparams',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 29, 8, 22, 30, 997119, tzinfo=utc), verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0442\u0441\u0447\u0435\u0442\u0430 \u043f\u0435\u0440\u0438\u043e\u0434\u0430 \u043f\u043e\u0432\u0442\u043e\u0440\u0435\u043d\u0438\u044f'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='is_repeating_clone',
            field=models.BooleanField(default=False, verbose_name='\u041a\u043b\u043e\u043d \u043f\u043e\u0432\u0442\u043e\u0440\u044f\u044e\u0449\u0435\u0439\u0441\u044f \u0437\u0430\u0434\u0430\u0447\u0438'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(default=b'in_work', max_length=20, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441 \u0437\u0430\u0434\u0430\u0447\u0438', choices=[(b'decline', '\u041e\u0442\u043a\u043b\u043e\u043d\u0435\u043d\u0430'), (b'awaiting', '\u041e\u0436\u0438\u0434\u0430\u0435\u0442 \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f'), (b'in_work', '\u0412\u044b\u043f\u043e\u043b\u043d\u044f\u0435\u0442\u0441\u044f'), (b'ready', '\u0413\u043e\u0442\u043e\u0432\u0430')]),
        ),
    ]
