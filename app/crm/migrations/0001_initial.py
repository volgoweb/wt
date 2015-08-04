# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_account_time_zone'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contact', '0001_initial'),
        ('task', '0008_auto_20150730_2207'),
    ]

    operations = [
        migrations.CreateModel(
            name='DealStatus',
            fields=[
                ('id', models.CharField(max_length=254, serialize=False, verbose_name=b'id', primary_key=True)),
                ('title', models.CharField(max_length=254, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SalesDeal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('desc', models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('budget', models.IntegerField(null=True, verbose_name='\u0411\u044e\u0434\u0436\u0435\u0442', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('edited', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f')),
                ('deleted', models.BooleanField(default=False, verbose_name='\u0423\u0434\u0430\u043b\u0435\u043d\u043d\u0430\u044f')),
                ('author', models.ForeignKey(related_name='sales_deal_of_author', verbose_name='\u0410\u0432\u0442\u043e\u0440', to=settings.AUTH_USER_MODEL)),
                ('client_company', models.ForeignKey(related_name='sales_deal', verbose_name='\u041a\u043e\u043c\u043f\u0430\u043d\u0438\u044f \u043a\u043b\u0438\u0435\u043d\u0442\u0430', to='contact.Company')),
                ('client_contact', models.ForeignKey(related_name='sales_deal', verbose_name='\u041a\u043e\u043d\u0442\u0430\u043a\u0442\u043d\u043e\u0435 \u043b\u0438\u0446\u043e \u043a\u043b\u0438\u0435\u043d\u0442\u0430', to='contact.Contact')),
                ('responsible', models.ForeignKey(related_name='sales_deal', verbose_name='\u041e\u0442\u0432\u0435\u0442\u0441\u0442\u0432\u0435\u043d\u043d\u044b\u0439', to='account.CompanyUnit')),
                ('responsible_user', models.ForeignKey(related_name='sales_deal', verbose_name='\u041e\u0442\u0432\u0435\u0442\u0441\u0442\u0432\u0435\u043d\u043d\u044b\u0439 (\u0430\u043a\u043a\u0430\u0443\u043d\u0442)', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(related_name='sales_deal', verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', to='crm.DealStatus')),
                ('tasks', models.ManyToManyField(related_name='sales_deal', verbose_name='\u0417\u0430\u0434\u0430\u0447\u0438', to='task.Task')),
            ],
        ),
    ]
