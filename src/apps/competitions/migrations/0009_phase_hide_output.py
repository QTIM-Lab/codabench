# Generated by Django 2.2.9 on 2020-02-07 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0008_auto_20200128_2236'),
    ]

    operations = [
        migrations.AddField(
            model_name='phase',
            name='hide_output',
            field=models.BooleanField(default=False),
        ),
    ]