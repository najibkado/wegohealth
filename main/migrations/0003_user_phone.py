# Generated by Django 3.2.15 on 2022-09-01 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20220831_0904'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default='080123456789', max_length=255),
            preserve_default=False,
        ),
    ]
