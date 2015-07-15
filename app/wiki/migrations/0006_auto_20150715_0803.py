# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wiki', '0005_wikipage_deleted'),
    ]

    operations = [
        migrations.CreateModel(
            name='WikiPageExtra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('editors_users', models.ManyToManyField(help_text='\u0421\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a\u0438, \u043a\u0442\u043e \u043c\u043e\u0436\u0435\u0442 \u0440\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0433\u043b\u0430\u0432\u0443 \u0438 \u0434\u043e\u0431\u0430\u0432\u043b\u044f\u0442\u044c \u0432\u043b\u043e\u0436\u0435\u043d\u043d\u044b\u0435 \u0433\u043b\u0430\u0432\u044b.', related_name='wiki_editor_user', verbose_name='\u0410\u0432\u0442\u043e\u0440\u044b \u0433\u043b\u0430\u0432\u044b', to=settings.AUTH_USER_MODEL)),
                ('performers_users', models.ManyToManyField(help_text='\u0421\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a\u0438, \u0434\u043b\u044f \u043a\u043e\u0433\u043e \u043f\u0440\u0435\u0434\u043d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u0430 \u0434\u0430\u043d\u043d\u0430\u044f \u0433\u043b\u0430\u0432\u0430.', related_name='wiki_performer_user', verbose_name='\u0418\u0441\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u0438', to=settings.AUTH_USER_MODEL)),
                ('subscribers_users', models.ManyToManyField(help_text='\u0421\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a\u0438, \u043a\u0442\u043e \u043c\u043e\u0436\u0435\u0442 \u0447\u0438\u0442\u0430\u0442\u044c \u0433\u043b\u0430\u0432\u0443 \u0438 \u043f\u043e\u043b\u0443\u0447\u0430\u0442\u044c \u0443\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u044f \u043e \u0435\u0435 \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0438.', related_name='wiki_subscriber_user', verbose_name='\u0427\u0438\u0442\u0430\u0442\u0435\u043b\u0438 \u0433\u043b\u0430\u0432\u044b', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='wikipage',
            name='editors',
            field=models.ManyToManyField(help_text='\u041e\u0442\u0434\u0435\u043b\u044b \u0438\u043b\u0438 \u0434\u043e\u043b\u0436\u043d\u043e\u0441\u0442\u0438, \u043a\u0442\u043e \u043c\u043e\u0436\u0435\u0442 \u0440\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0433\u043b\u0430\u0432\u0443 \u0438 \u0434\u043e\u0431\u0430\u0432\u043b\u044f\u0442\u044c \u0432\u043b\u043e\u0436\u0435\u043d\u043d\u044b\u0435 \u0433\u043b\u0430\u0432\u044b.', related_name='wiki_editor', verbose_name='\u0410\u0432\u0442\u043e\u0440\u044b \u0433\u043b\u0430\u0432\u044b', to='account.CompanyUnit'),
        ),
        migrations.AlterField(
            model_name='wikipage',
            name='performers',
            field=models.ManyToManyField(help_text='\u041e\u0442\u0434\u0435\u043b\u044b \u0438\u043b\u0438 \u0434\u043e\u043b\u0436\u043d\u043e\u0441\u0442\u0438, \u0434\u043b\u044f \u043a\u043e\u0433\u043e \u043f\u0440\u0435\u0434\u043d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u0430 \u0434\u0430\u043d\u043d\u0430\u044f \u0433\u043b\u0430\u0432\u0430.', related_name='wiki_performer', verbose_name='\u0418\u0441\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u0438', to='account.CompanyUnit'),
        ),
        migrations.AlterField(
            model_name='wikipage',
            name='subscribers',
            field=models.ManyToManyField(help_text='\u041e\u0442\u0434\u0435\u043b\u044b \u0438\u043b\u0438 \u0434\u043e\u043b\u0436\u043d\u043e\u0441\u0442\u0438, \u043a\u0442\u043e \u043c\u043e\u0436\u0435\u0442 \u0447\u0438\u0442\u0430\u0442\u044c \u0433\u043b\u0430\u0432\u0443 \u0438 \u043f\u043e\u043b\u0443\u0447\u0430\u0442\u044c \u0443\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u044f \u043e \u0435\u0435 \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0438.', related_name='wiki_subscriber', verbose_name='\u0427\u0438\u0442\u0430\u0442\u0435\u043b\u0438 \u0433\u043b\u0430\u0432\u044b', to='account.CompanyUnit'),
        ),
        migrations.AddField(
            model_name='wikipageextra',
            name='wiki_page',
            field=models.ForeignKey(related_name='extra', to='wiki.WikiPage'),
        ),
    ]
