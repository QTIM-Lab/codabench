# Generated by Django 2.2.17 on 2024-03-04 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auth_Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('client_id', models.CharField(max_length=255)),
                ('client_secret', models.CharField(max_length=255)),
                ('authorization_url', models.CharField(max_length=255)),
                ('token_url', models.CharField(max_length=255)),
                ('user_info_url', models.CharField(max_length=255)),
                ('redirect_url', models.CharField(max_length=255)),
                ('button_bg_color', models.CharField(default='#2C3E4C', max_length=20)),
                ('button_text_color', models.CharField(default='#FFFFFF', max_length=20)),
            ],
        ),
    ]
