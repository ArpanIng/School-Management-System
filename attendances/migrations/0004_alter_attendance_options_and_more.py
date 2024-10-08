# Generated by Django 4.2.15 on 2024-08-14 11:43

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0003_alter_class_is_active"),
        ("attendances", "0003_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="attendance",
            options={"ordering": ["attendance_date", "course_class"]},
        ),
        migrations.RemoveConstraint(
            model_name="attendance",
            name="unique_attendance_per_student_per_course_per_date",
        ),
        migrations.RemoveIndex(
            model_name="attendance",
            name="attendances_attenda_ce71ab_idx",
        ),
        migrations.RemoveField(
            model_name="attendance",
            name="course",
        ),
        migrations.AddField(
            model_name="attendance",
            name="course_class",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="attendances",
                to="courses.class",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="attendance",
            name="attendance_date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddIndex(
            model_name="attendance",
            index=models.Index(
                fields=["attendance_date", "course_class"],
                name="attendances_attenda_fe41f8_idx",
            ),
        ),
        migrations.AddConstraint(
            model_name="attendance",
            constraint=models.UniqueConstraint(
                fields=("course_class", "student", "attendance_date"),
                name="unique_attendance_per_student_per_class_per_date",
            ),
        ),
    ]
