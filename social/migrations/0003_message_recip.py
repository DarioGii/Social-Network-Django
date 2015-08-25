# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_auto_20150329_1948'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='recip',
            field=models.CharField(default=datetime.datetime(2015, 3, 29, 21, 0, 56, 150159, tzinfo=utc), max_length=16),
            preserve_default=False,
        ),
    ]
