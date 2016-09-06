# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-31 18:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('query', '0005_auto_20160831_1439'),
    ]

    operations = [
        migrations.RenameField(
            model_name='databasemessage',
            old_name='db_database',
            new_name='db_databa',
        ),
        migrations.RenameField(
            model_name='databasemessage',
            old_name='db_tableenvname',
            new_name='db_databaenvname',
        ),
        migrations.RenameField(
            model_name='databasemessage',
            old_name='db_tableid',
            new_name='db_databaid',
        ),
        migrations.RenameField(
            model_name='querymessage',
            old_name='qu_dbid',
            new_name='qu_databaid',
        ),
        migrations.RemoveField(
            model_name='databasemessage',
            name='db_table',
        ),
        migrations.RemoveField(
            model_name='querymessage',
            name='qu_tableid',
        ),
    ]
