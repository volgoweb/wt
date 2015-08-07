# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='performers',
            field=models.ManyToManyField(to='account.CompanyUnit', null=True, verbose_name='\u0418\u0441\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u0438', blank=True),
        ),
    ]
