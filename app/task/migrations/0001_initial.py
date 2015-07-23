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
            name='RepeatParams',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('period', models.CharField(max_length=20, verbose_name='\u041f\u0435\u0440\u0438\u043e\u0434 \u043f\u043e\u0432\u0442\u043e\u0440\u0435\u043d\u0438\u044f', choices=[(b'day', '\u041a\u0430\u0436\u0434\u044b\u0439 \u0434\u0435\u043d\u044c'), (b'week', '\u041a\u0430\u0436\u0434\u0443\u044e \u043d\u0435\u0434\u0435\u043b\u044e'), (b'month_by_day', '\u041a\u0430\u0436\u0434\u044b\u0439 \u043c\u0435\u0441\u044f\u0446 (\u043f\u043e \u0434\u043d\u044e \u043c\u0435\u0441\u044f\u0446\u0430)'), (b'year_by_day', '\u041a\u0430\u0436\u0434\u044b\u0439 \u0433\u043e\u0434 (\u043f\u043e \u0434\u043d\u044e \u043c\u0435\u0441\u044f\u0446\u0430)')])),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('due_date', models.DateTimeField(null=True, verbose_name='\u041a\u0440\u0430\u0439\u043d\u0438\u0439 \u0441\u0440\u043e\u043a', blank=True)),
                ('status', models.CharField(default=b'in_work', max_length=20, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441 \u0437\u0430\u0434\u0430\u0447\u0438', choices=[(b'decline', '\u041e\u0442\u043a\u043b\u043e\u043d\u0435\u043d\u0430'), (b'in_work', '\u0412 \u0440\u0430\u0431\u043e\u0442\u0435'), (b'ready', '\u0413\u043e\u0442\u043e\u0432\u0430')])),
                ('is_favorite', models.BooleanField(default=False, verbose_name='\u0418\u0437\u0431\u0440\u0430\u043d\u043d\u0430\u044f')),
                ('deleted', models.BooleanField(default=False, verbose_name='\u0423\u0434\u0430\u043b\u0435\u043d\u043d\u0430\u044f')),
                ('author', models.ForeignKey(related_name='task_author', verbose_name='\u0410\u0432\u0442\u043e\u0440', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='TaskFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=b'files', verbose_name='\u0424\u0430\u0439\u043b')),
            ],
        ),
        migrations.CreateModel(
            name='TaskStep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('completed', models.BooleanField(default=False, verbose_name='\u0421\u0434\u0435\u043b\u0430\u043d')),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('desc', models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('date', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0438\u0441\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaskTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0437\u0430\u0434\u0430\u0447\u0438')),
                ('desc', models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0437\u0430\u0434\u0430\u0447\u0438', blank=True)),
                ('step_id', models.PositiveIntegerField(null=True, blank=True)),
                ('files', models.ManyToManyField(related_name='tasktemplate_files', verbose_name='\u0412\u043b\u043e\u0436\u0435\u043d\u0438\u044f', to='task.TaskFile')),
                ('performer', models.ForeignKey(related_name='tasktemplate_performer', verbose_name='\u0418\u0441\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL)),
                ('polymorphic_ctype', models.ForeignKey(related_name='polymorphic_task.tasktemplate_set+', editable=False, to='contenttypes.ContentType', null=True)),
                ('repeat_params', models.ForeignKey(related_name='repeat_params', verbose_name='\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u043f\u043e\u0432\u0442\u043e\u0440\u0435\u043d\u0438\u044f', blank=True, to='task.RepeatParams', null=True)),
                ('step_type', models.ForeignKey(related_name='tasktemplate_step_type', blank=True, to='contenttypes.ContentType', null=True)),
                ('task_steps', models.ManyToManyField(related_name='tasktemplate_task_steps', verbose_name='\u0428\u0430\u0433\u0438 \u0437\u0430\u0434\u0430\u0447\u0438', to='task.TaskStep')),
            ],
            options={
                'abstract': False,
            },
            bases=(helper.models.FieldsLabelsMixin, models.Model),
        ),
        migrations.AddField(
            model_name='task',
            name='template',
            field=models.ForeignKey(related_name='template', blank=True, to='task.TaskTemplate', help_text='\u0412\u0441\u0435 \u0431\u0430\u0437\u043e\u0432\u044b\u0435 \u043f\u043e\u043b\u044f, \u043a\u043e\u0442\u043e\u0440\u044b\u0435 \u043c\u043e\u0433\u0443\u0442 \u0431\u044b\u0442\u044c \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u044b \u0432\u043e \u0432\u0441\u0435\u0445 \u043f\u043e\u0432\u0442\u043e\u0440\u044f\u044e\u0449\u0438\u0445\u0441\u044f \u044d\u043a\u0437\u0435\u043c\u043f\u043b\u044f\u0440\u0430\u0445 \u0437\u0430\u0434\u0430\u0447.', null=True, verbose_name='\u0428\u0430\u0431\u043b\u043e\u043d'),
        ),
    ]
