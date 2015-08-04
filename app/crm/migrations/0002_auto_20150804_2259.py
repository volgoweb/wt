# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_account_time_zone'),
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salesdeal',
            name='responsible_user',
        ),
        migrations.AddField(
            model_name='salesdeal',
            name='responsible_unit',
            field=models.ForeignKey(related_name='sales_deal', default=1, verbose_name='\u041e\u0442\u0432\u0435\u0442\u0441\u0442\u0432\u0435\u043d\u043d\u044b\u0439', to='account.CompanyUnit'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='salesdeal',
            name='responsible',
            field=models.ForeignKey(related_name='sales_deal', verbose_name='\u041e\u0442\u0432\u0435\u0442\u0441\u0442\u0432\u0435\u043d\u043d\u044b\u0439 (\u0430\u043a\u043a\u0430\u0443\u043d\u0442)', to=settings.AUTH_USER_MODEL),
        ),
    ]
