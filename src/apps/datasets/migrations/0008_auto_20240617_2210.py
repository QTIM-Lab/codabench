# Generated by Django 2.2.17 on 2024-06-17 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0007_auto_20230609_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='type',
            field=models.CharField(choices=[('ingestion_program', 'Ingestion Program'), ('input_data', 'Input Data'), ('public_data', 'Public Data'), ('reference_data', 'Reference Data'), ('scoring_program', 'Scoring Program'), ('starting_kit', 'Starting Kit'), ('competition_bundle', 'Competition Bundle'), ('submission', 'Submission'), ('solution', 'Solution'), ('docker_image', 'Docker_Image')], max_length=64),
        ),
    ]