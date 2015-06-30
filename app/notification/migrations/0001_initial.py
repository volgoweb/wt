# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0431\u044b\u0442\u0438\u044f')),
                ('readed', models.BooleanField(default=False, verbose_name='\u041f\u0440\u043e\u0447\u0438\u0442\u0430\u043d\u043e')),
                ('text', models.TextField(verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0441\u043e\u0431\u044b\u0442\u0438\u044f')),
                ('obj_id', models.PositiveIntegerField(null=True, blank=True)),
                ('obj_type', models.ForeignKey(related_name='obj_type', blank=True, to='contenttypes.ContentType', null=True)),
                ('polymorphic_ctype', models.ForeignKey(related_name='polymorphic_notification.notification_set+', editable=False, to='contenttypes.ContentType', null=True)),
                ('subscriber', models.ForeignKey(verbose_name='\u041f\u043e\u0434\u043f\u0438\u0441\u0447\u0438\u043a', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
