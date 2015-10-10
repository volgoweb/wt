# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_auto_20151008_0729'),
        ('task', '0008_auto_20150730_2207'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasktemplate',
            name='contact',
            field=models.ForeignKey(verbose_name='\u041a\u043e\u043d\u0442\u0430\u043a\u0442', blank=True, to='contact.Contact', null=True),
        ),
    ]
