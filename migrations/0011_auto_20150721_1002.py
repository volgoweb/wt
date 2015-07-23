# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comment', '0001_initial'),
        ('task', '0010_auto_20150718_1339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasktemplate',
            name='task_ptr',
        ),
        migrations.AddField(
            model_name='tasktemplate',
            name='author',
            field=models.ForeignKey(related_name='tasktemplate_author', default=1, verbose_name='\u0410\u0432\u0442\u043e\u0440', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tasktemplate',
            name='comments',
            field=models.ManyToManyField(related_name='tasktemplate_comments', verbose_name='\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439', to='comment.Comment'),
        ),
        migrations.AddField(
            model_name='tasktemplate',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 21, 15, 2, 14, 661211, tzinfo=utc), verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tasktemplate',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='\u0423\u0434\u0430\u043b\u0435\u043d\u043d\u0430\u044f'),
        ),
        migrations.AddField(
            model_name='tasktemplate',
            name='desc',
            field=models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0437\u0430\u0434\u0430\u0447\u0438', blank=True),
        ),
        migrations.AddField(
            model_name='tasktemplate',
            name='due_date',
            field=models.DateTimeField(null=True, verbose_name='\u041a\u0440\u0430\u0439\u043d\u0438\u0439 \u0441\u0440\u043e\u043a', blank=True),
        ),
        migrations.AddField(
            model_name='tasktemplate',
            name='files',
            field=models.ManyToManyField(related_name='tasktemplate_files', verbose_name='\u0412\u043b\u043e\u0436\u0435\u043d\u0438\u044f', to='task.TaskFile'),
        ),
        migrations.AddField(
            model_name='tasktemplate',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=1, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tasktemplate',
            name='is_favorite',
            field=models.BooleanField(default=False, verbose_name='\u0418\u0437\u0431\u0440\u0430\u043d\u043d\u0430\u044f'),
        ),
        migrations.AddField(
            model_name='tasktemplate',
            name='performer',
            field=models.ForeignKey(related_name='tasktemplate_performer', default=1, verbose_name='\u0418\u0441\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tasktemplate',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_task.tasktemplate_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='tasktemplate',
            name='status',
            field=models.CharField(default=b'in_work', max_length=20, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441 \u0437\u0430\u0434\u0430\u0447\u0438', choices=[(b'decline', '\u041e\u0442\u043a\u043b\u043e\u043d\u0435\u043d\u0430'), (b'in_work', '\u0412 \u0440\u0430\u0431\u043e\u0442\u0435'), (b'ready', '\u0413\u043e\u0442\u043e\u0432\u0430')]),
        ),
        migrations.AddField(
            model_name='tasktemplate',
            name='step_id',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='tasktemplate',
            name='step_type',
            field=models.ForeignKey(related_name='tasktemplate_step_type', blank=True, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='tasktemplate',
            name='task_steps',
            field=models.ManyToManyField(related_name='tasktemplate_task_steps', verbose_name='\u0428\u0430\u0433\u0438 \u0437\u0430\u0434\u0430\u0447\u0438', to='task.TaskStep'),
        ),
        migrations.AddField(
            model_name='tasktemplate',
            name='title',
            field=models.CharField(default=1, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0437\u0430\u0434\u0430\u0447\u0438'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='author',
            field=models.ForeignKey(related_name='task_author', verbose_name='\u0410\u0432\u0442\u043e\u0440', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='comments',
            field=models.ManyToManyField(related_name='task_comments', verbose_name='\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439', to='comment.Comment'),
        ),
        migrations.AlterField(
            model_name='task',
            name='files',
            field=models.ManyToManyField(related_name='task_files', verbose_name='\u0412\u043b\u043e\u0436\u0435\u043d\u0438\u044f', to='task.TaskFile'),
        ),
        migrations.AlterField(
            model_name='task',
            name='step_type',
            field=models.ForeignKey(related_name='task_step_type', blank=True, to='contenttypes.ContentType', null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_steps',
            field=models.ManyToManyField(related_name='task_task_steps', verbose_name='\u0428\u0430\u0433\u0438 \u0437\u0430\u0434\u0430\u0447\u0438', to='task.TaskStep'),
        ),
    ]
