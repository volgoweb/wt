# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileitem',
            name='owner_id',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='fileitem',
            name='owner_type',
            field=models.ForeignKey(related_name='owner_type', blank=True, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='fileitem',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_core.fileitem_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
    ]
