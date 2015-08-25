# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0004_auto_20150330_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='time',
            field=models.DateField(auto_now=True, default=datetime.datetime(2015, 3, 31, 21, 21, 4, 54405, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
