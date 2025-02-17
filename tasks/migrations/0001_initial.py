# Generated by Django 5.1.4 on 2024-12-25 08:14

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0003_remove_project_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('reference', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('is_completed', models.BooleanField(default=False)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='projects.project')),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
                'ordering': ['-created_at'],
            },
        ),
    ]
