# Generated by Django 2.1.2 on 2019-11-04 21:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('vhost', models.UUIDField(unique=True)),
                ('is_public', models.BooleanField(default=False)),
                ('created_when', models.DateTimeField(default=django.utils.timezone.now)),
                ('organizers', models.ManyToManyField(blank=True, related_name='organized_queues', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='queues', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]