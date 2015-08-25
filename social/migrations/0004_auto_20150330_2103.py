# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0003_message_recip'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='pm',
        ),
        migrations.AddField(
            model_name='message',
            name='private',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='author',
            field=models.ForeignKey(to='social.Member', related_name='author'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='recip',
            field=models.ForeignKey(to='social.Member', related_name='recip'),
            preserve_default=True,
        ),
    ]
