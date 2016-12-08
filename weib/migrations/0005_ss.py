# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weib', '0004_auto_20161206_2325'),
    ]

    operations = [
        migrations.CreateModel(
            name='ss',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=50)),
                ('img', models.ImageField(upload_to='upload')),
                ('status', models.TextField()),
            ],
        ),
    ]
