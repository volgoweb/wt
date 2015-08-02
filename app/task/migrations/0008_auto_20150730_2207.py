# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0007_tasktemplate_performer_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(default=b'in_work', max_length=20, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441 \u0437\u0430\u0434\u0430\u0447\u0438', choices=[(b'decline', '\u041e\u0442\u043a\u043b\u043e\u043d\u0435\u043d\u0430 \u0438\u0441\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u0435\u043c'), (b'awaiting', '\u041e\u0436\u0438\u0434\u0430\u0435\u0442 \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f'), (b'in_work', '\u0412\u044b\u043f\u043e\u043b\u043d\u044f\u0435\u0442\u0441\u044f'), (b'ready', '\u0413\u043e\u0442\u043e\u0432\u0430')]),
        ),
        migrations.AlterField(
            model_name='tasktemplate',
            name='performer_unit',
            field=models.ForeignKey(related_name='tasktemplate_performer_unit', verbose_name='\u0418\u0441\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c', to='account.CompanyUnit'),
        ),
    ]
