# Generated by Django 5.1.4 on 2024-12-25 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='date',
            field=models.DateField(default='2024-12-24'),
            preserve_default=False,
        ),
    ]
