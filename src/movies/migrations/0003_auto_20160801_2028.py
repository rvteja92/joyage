# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20160801_1544'),
    ]

    operations = [
        migrations.RenameField(
            model_name='show',
            old_name='theatre',
            new_name='theater',
        ),
    ]
