# Generated by Django 3.2.15 on 2022-08-27 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20220825_2256'),
    ]

    operations = [
        migrations.AddField(
            model_name='drug',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
