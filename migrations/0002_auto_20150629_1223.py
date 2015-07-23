# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comment', '0001_initial'),
        ('core', '0001_initial'),
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='comment',
        ),
        migrations.AddField(
            model_name='task',
            name='author',
            field=models.ForeignKey(default=1, verbose_name='\u0410\u0432\u0442\u043e\u0440', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='comments',
            field=models.ManyToManyField(to='comment.Comment', verbose_name='\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439'),
        ),
        migrations.AddField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(null=True, verbose_name='\u041a\u0440\u0430\u0439\u043d\u0438\u0439 \u0441\u0440\u043e\u043a', blank=True),
        ),
        migrations.AddField(
            model_name='task',
            name='files',
            field=models.ManyToManyField(to='core.FileItem', verbose_name='\u0412\u043b\u043e\u0436\u0435\u043d\u0438\u044f'),
        ),
    ]
