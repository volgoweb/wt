# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('text', models.TextField(max_length=5000)),
                ('deleted', models.BooleanField(default=False, verbose_name='\u0423\u0434\u0430\u043b\u0435\u043d\u043d\u0430\u044f')),
                ('author', models.ForeignKey(verbose_name='\u0410\u0432\u0442\u043e\u0440', to=settings.AUTH_USER_MODEL)),
                ('files', models.ManyToManyField(to='core.FileItem', verbose_name='\u0412\u043b\u043e\u0436\u0435\u043d\u0438\u044f')),
            ],
        ),
    ]
