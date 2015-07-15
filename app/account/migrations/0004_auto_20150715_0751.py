# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20150715_0547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='job',
            field=models.ForeignKey(related_name='user_job', verbose_name='\u0414\u043e\u043b\u0436\u043d\u043e\u0441\u0442\u044c', blank=True, to='account.CompanyUnit', null=True),
        ),
    ]
