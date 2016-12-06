# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weib', '0002_auto_20161206_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='uid',
            field=models.UUIDField(default=0),
        ),
    ]
