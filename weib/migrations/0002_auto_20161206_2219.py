# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weib', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='uid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='users',
            name='expired_time',
            field=models.FloatField(),
        ),
    ]
