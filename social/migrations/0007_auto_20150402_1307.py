# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0006_auto_20150331_2125'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('time',)},
        ),
    ]
