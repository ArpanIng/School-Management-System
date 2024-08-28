# Generated by Django 4.2.15 on 2024-08-14 09:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("attendances", "0001_initial"),
        ("courses", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="attendance",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="attendances",
                to="courses.course",
            ),
        ),
    ]
