# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0003_contact_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='is_partner',
            field=models.BooleanField(default=False, verbose_name='\u041f\u0430\u0440\u0442\u043d\u0435\u0440'),
        ),
    ]
