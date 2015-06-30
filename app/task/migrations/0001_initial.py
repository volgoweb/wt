# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import helper.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0437\u0430\u0434\u0430\u0447\u0438')),
                ('desc', models.TextField(verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0437\u0430\u0434\u0430\u0447\u0438')),
                ('comment', models.TextField(null=True, verbose_name='\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439', blank=True)),
                ('step_id', models.PositiveIntegerField(null=True, blank=True)),
                ('status', models.CharField(default=b'in_work', max_length=20, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441 \u0437\u0430\u0434\u0430\u0447\u0438', choices=[(b'decline', '\u041e\u0442\u043a\u043b\u043e\u043d\u0435\u043d\u0430'), (b'in_work', '\u0412 \u0440\u0430\u0431\u043e\u0442\u0435'), (b'ready', '\u0413\u043e\u0442\u043e\u0432\u0430')])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('deleted', models.BooleanField(default=False, verbose_name='\u0423\u0434\u0430\u043b\u0435\u043d\u043d\u0430\u044f')),
                ('performer', models.ForeignKey(related_name='task_performer', verbose_name='\u0418\u0441\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL)),
                ('polymorphic_ctype', models.ForeignKey(related_name='polymorphic_task.task_set+', editable=False, to='contenttypes.ContentType', null=True)),
                ('step_type', models.ForeignKey(related_name='step_type', blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'ordering': ['-created'],
            },
            bases=(helper.models.FieldsLabelsMixin, models.Model),
        ),
    ]
