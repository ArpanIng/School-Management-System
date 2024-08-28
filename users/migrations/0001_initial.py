# Generated by Django 4.2.15 on 2024-08-14 09:28

import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import users.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("academics", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_of_birth", models.DateField(null=True)),
                ("phone_number", models.CharField(max_length=10)),
                ("address", models.CharField(max_length=100)),
                (
                    "avatar",
                    models.ImageField(
                        default="default_profile.jpg", upload_to="Users Avatars/"
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female"), ("O", "Other")],
                        max_length=1,
                    ),
                ),
                (
                    "marital_status",
                    models.CharField(
                        choices=[("S", "Single"), ("M", "Married")],
                        default="S",
                        max_length=1,
                    ),
                ),
                ("post_code", models.CharField(default="44600", max_length=10)),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("Koshi", "Koshi"),
                            ("Madhesh", "Madhesh"),
                            ("Bagmati", "Bagmati"),
                            ("Gandaki", "Gandaki"),
                            ("Lumbini", "Lumbini"),
                            ("Karnali", "Karnali"),
                            ("Sudurpaschim", "Sudurpaschim"),
                        ],
                        max_length=15,
                    ),
                ),
                (
                    "city",
                    models.CharField(blank=True, default="Kathmandu", max_length=50),
                ),
                ("country", models.CharField(default="Nepal", max_length=100)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "student_id",
                    models.PositiveIntegerField(
                        unique=True, validators=[users.models.validate_id_length]
                    ),
                ),
                (
                    "parent_contact",
                    models.CharField(
                        blank=True, default="", max_length=10, unique=True
                    ),
                ),
                ("guardian", models.CharField(max_length=100)),
                (
                    "guardian_relation",
                    models.CharField(
                        choices=[
                            ("FTH", "Father"),
                            ("MTH", "Mother"),
                            ("GFA", "Grandfather"),
                            ("GMO", "Grandmother"),
                            ("UNC", "Uncle"),
                            ("AUN", "Aunt"),
                            ("BRO", "Brother"),
                            ("SIS", "Sister"),
                            ("OTH", "Other"),
                        ],
                        default="FTH",
                        max_length=3,
                    ),
                ),
                ("enrollment_date", models.DateField()),
                ("graduation_date", models.DateField()),
                (
                    "profile",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="users.profile"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Instructor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "employee_id",
                    models.PositiveIntegerField(
                        unique=True, validators=[users.models.validate_id_length]
                    ),
                ),
                (
                    "qualification",
                    models.CharField(
                        choices=[
                            ("PHD", "PhD"),
                            ("MASTERS", "Master's Degree"),
                            ("BACHELORS", "Bachelor's Degree"),
                            ("ASSOCIATE", "Associate Degree"),
                        ],
                        max_length=20,
                    ),
                ),
                ("date_of_joining", models.DateField()),
                (
                    "department",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="instructors",
                        to="academics.department",
                    ),
                ),
                (
                    "profile",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="users.profile"
                    ),
                ),
            ],
        ),
    ]
