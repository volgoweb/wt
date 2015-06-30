# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('route', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('baseroute_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='route.BaseRoute')),
                ('application_desc', models.CharField(max_length=20000, null=True, blank=True)),
                ('manager', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('route.baseroute',),
        ),
        migrations.CreateModel(
            name='Step1',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('route.basestep',),
        ),
        migrations.CreateModel(
            name='Step2',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('route.basestep',),
        ),
    ]
