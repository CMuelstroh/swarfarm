# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('herders', '0034_summoner_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='monster',
            name='summonerswar_co_url',
            field=models.URLField(null=True, blank=True),
        ),
    ]
