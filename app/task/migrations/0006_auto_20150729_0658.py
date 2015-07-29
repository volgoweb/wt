# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('task', '0005_auto_20150729_0550'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasktemplate',
            name='repeat_params',
        ),
        migrations.AddField(
            model_name='tasktemplate',
            name='author',
            field=models.ForeignKey(related_name='tasktemplate_author', default=1, verbose_name='\u0410\u0432\u0442\u043e\u0440', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tasktemplate',
            name='due_date',
            field=models.DateTimeField(null=True, verbose_name='\u041a\u0440\u0430\u0439\u043d\u0438\u0439 \u0441\u0440\u043e\u043a', blank=True),
        ),
        migrations.AddField(
            model_name='tasktemplate',
            name='period',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='\u041f\u0435\u0440\u0438\u043e\u0434 \u043f\u043e\u0432\u0442\u043e\u0440\u0435\u043d\u0438\u044f', choices=[(b'day', '\u041a\u0430\u0436\u0434\u044b\u0439 \u0434\u0435\u043d\u044c'), (b'week', '\u041a\u0430\u0436\u0434\u0443\u044e \u043d\u0435\u0434\u0435\u043b\u044e'), (b'month_by_day', '\u041a\u0430\u0436\u0434\u044b\u0439 \u043c\u0435\u0441\u044f\u0446 (\u043f\u043e \u0434\u043d\u044e \u043c\u0435\u0441\u044f\u0446\u0430)'), (b'year_by_day', '\u041a\u0430\u0436\u0434\u044b\u0439 \u0433\u043e\u0434 (\u043f\u043e \u0434\u043d\u044e \u043c\u0435\u0441\u044f\u0446\u0430)')]),
        ),
        migrations.DeleteModel(
            name='RepeatParams',
        ),
    ]
