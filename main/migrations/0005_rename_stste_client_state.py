# Generated by Django 3.2.15 on 2022-09-02 22:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20220902_2249'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='stste',
            new_name='state',
        ),
    ]