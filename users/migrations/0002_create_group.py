# Generated by Django 4.2.15 on 2024-08-14 09:29

from django.db import migrations


def create_groups(apps, schema_editor):
    # We can't import the models directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    # local apps models
    Department = apps.get_model("academics", "Department")
    Course = apps.get_model("courses", "Course")
    Class = apps.get_model("courses", "Class")

    # get the content type for the models
    department_ct = ContentType.objects.get_for_model(Department)
    course_ct = ContentType.objects.get_for_model(Course)
    class_ct = ContentType.objects.get_for_model(Class)

    # create groups
    admin_group, _ = Group.objects.get_or_create(name="Admin")
    instructor_group, _ = Group.objects.get_or_create(name="Instructor")
    student_group, _ = Group.objects.get_or_create(name="Student")

    # get the permissions for each models
    department_permissions = Permission.objects.filter(content_type=department_ct)
    course_permissions = Permission.objects.filter(content_type=course_ct)
    class_permissions = Permission.objects.filter(content_type=class_ct)

    # assign the permissions to the 'Admin' group
    admin_group.permissions.add(*department_permissions)
    admin_group.permissions.add(*course_permissions)
    admin_group.permissions.add(*class_permissions)

    # assign the permissions to the 'Instructor' group
    instructor_permissions = Permission.objects.filter(
        content_type__in=[course_ct, class_ct],
        codename__in=["view_course", "view_class", "add_class", "change_class"],
    )
    instructor_group.permissions.add(*instructor_permissions)

    # assign the permissions to the 'Student' group
    student_permissions = Permission.objects.filter(
        content_type__in=[course_ct, class_ct],
        codename__in=["view_course", "view_class"],
    )
    student_group.permissions.add(*student_permissions)


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
