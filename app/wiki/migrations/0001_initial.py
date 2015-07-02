# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tagging_autosuggest.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WikiPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a')),
                ('text', models.TextField(max_length=50000, verbose_name='\u0422\u0435\u043a\u0441\u0442')),
                ('tags', tagging_autosuggest.fields.TagAutosuggestField(default='', max_length=100, blank=True)),
            ],
        ),
    ]
