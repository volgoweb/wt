# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseRoute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('polymorphic_ctype', models.ForeignKey(related_name='polymorphic_route.baseroute_set+', editable=False, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BaseStep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('results', models.TextField(null=True, blank=True)),
                ('status', models.CharField(default=b'not_run', max_length=20, choices=[(b'not_run', b'not_run'), (b'in_work', b'in_work'), (b'ready', b'ready')])),
                ('task_id', models.PositiveIntegerField(null=True, blank=True)),
                ('route_id', models.PositiveIntegerField()),
                ('polymorphic_ctype', models.ForeignKey(related_name='polymorphic_route.basestep_set+', editable=False, to='contenttypes.ContentType', null=True)),
                ('route_type', models.ForeignKey(related_name='route_type', blank=True, to='contenttypes.ContentType', null=True)),
                ('task_type', models.ForeignKey(related_name='task_type', blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
