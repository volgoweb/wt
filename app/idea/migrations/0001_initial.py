# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=254, verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a')),
                ('desc', models.TextField(max_length=15000, null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('edited', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f')),
                ('deleted', models.BooleanField(default=False, verbose_name='\u0423\u0434\u0430\u043b\u0435\u043d\u043d\u0430\u044f')),
                ('author', models.ForeignKey(related_name='idea_of_author', verbose_name='\u0410\u0432\u0442\u043e\u0440', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
