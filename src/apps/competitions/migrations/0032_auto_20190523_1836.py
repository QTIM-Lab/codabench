# Generated by Django 2.1.2 on 2019-05-23 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0031_auto_20190521_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='registration_auto_approve',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='competition',
            name='registration_required',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='competition',
            name='terms',
            field=models.TextField(blank=True, null=True),
        ),
    ]