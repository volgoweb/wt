# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150712_1311'),
        ('task', '0005_remove_task_files'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=b'files', verbose_name='\u0424\u0430\u0439\u043b')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='files',
            field=models.ManyToManyField(to='core.FileItem', verbose_name='\u0412\u043b\u043e\u0436\u0435\u043d\u0438\u044f'),
        ),
    ]
