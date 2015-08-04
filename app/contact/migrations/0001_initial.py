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
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('desc', models.TextField(help_text=b'\xd0\x9e\xd0\xb1\xd1\x89\xd0\xb5\xd0\xb5 \xd0\xbe\xd0\xbf\xd0\xb8\xd1\x81\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5, \xd1\x80\xd0\xb5\xd0\xb6\xd0\xb8\xd0\xbc \xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd1\x8b, \xd0\xbe\xd0\xb1\xd1\x89\xd0\xb8\xd0\xb5 \xd0\xba\xd0\xbe\xd0\xbd\xd1\x82\xd0\xb0\xd0\xba\xd1\x82\xd1\x8b \xd0\xb8 \xd0\xb0\xd0\xb4\xd1\x80\xd0\xb5\xd1\x81\xd0\xb0 \xd0\xbe\xd1\x84\xd0\xb8\xd1\x81\xd0\xbe\xd0\xb2.', null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('is_lead', models.BooleanField(default=False, verbose_name='\u041f\u043e\u0442\u0435\u043d\u0446\u0438\u0430\u043b\u044c\u043d\u044b\u0439 \u043a\u043b\u0438\u0435\u043d\u0442')),
                ('is_client', models.BooleanField(default=False, verbose_name='\u041a\u043b\u0438\u0435\u043d\u0442')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('changed', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f')),
                ('deleted', models.BooleanField(default=False, verbose_name='\u0423\u0434\u0430\u043b\u0435\u043d\u043d\u044b\u0439')),
                ('author', models.ForeignKey(verbose_name='\u0410\u0432\u0442\u043e\u0440', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=255, verbose_name='\u041f\u043e\u043b\u043d\u043e\u0435 \u0438\u043c\u044f')),
                ('desc', models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('phone', models.CharField(max_length=30, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d')),
                ('mobile_phone', models.CharField(max_length=30, verbose_name='\u041c\u043e\u0431\u0438\u043b\u044c\u043d\u044b\u0439 \u0442\u0435\u043b.')),
                ('is_lead', models.BooleanField(default=False, verbose_name='\u041f\u043e\u0442\u0435\u043d\u0446\u0438\u0430\u043b\u044c\u043d\u044b\u0439 \u043a\u043b\u0438\u0435\u043d\u0442')),
                ('is_client', models.BooleanField(default=False, verbose_name='\u041a\u043b\u0438\u0435\u043d\u0442')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('changed', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f')),
                ('deleted', models.BooleanField(default=False, verbose_name='\u0423\u0434\u0430\u043b\u0435\u043d\u043d\u044b\u0439')),
                ('author', models.ForeignKey(verbose_name='\u0410\u0432\u0442\u043e\u0440', to=settings.AUTH_USER_MODEL)),
                ('company', models.ForeignKey(verbose_name='\u041a\u043e\u043c\u043f\u0430\u043d\u0438\u044f', blank=True, to='contact.Company', null=True)),
            ],
        ),
    ]
