# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20150730_0945'),
        ('task', '0006_auto_20150729_0658'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasktemplate',
            name='performer_unit',
            field=models.ForeignKey(related_name='tasktemplate_performer_unit', default=1, verbose_name='\u0418\u0441\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c (\u0434\u043e\u043b\u0436\u043d\u043e\u0441\u0442\u043d\u0430\u044f \u0435\u0434\u0438\u043d\u0438\u0446\u0430)', to='account.CompanyUnit'),
            preserve_default=False,
        ),
    ]
