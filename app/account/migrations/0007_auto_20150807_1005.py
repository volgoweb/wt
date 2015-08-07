# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_account_time_zone'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='department',
            field=models.ForeignKey(related_name='account_of_department', verbose_name='\u041e\u0442\u0434\u0435\u043b', blank=True, to='account.CompanyUnit', null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='job',
            field=models.ForeignKey(related_name='account_of_job', verbose_name='\u0414\u043e\u043b\u0436\u043d\u043e\u0441\u0442\u044c', blank=True, to='account.CompanyUnit', null=True),
        ),
    ]
