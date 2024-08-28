from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.query import Q


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Email field is required.")

        if not username:
            raise ValueError("Username field is required.")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        user = self.create_user(email, username, password, **extra_fields)
        user.save(using=self._db)

        # Add user to the 'Admin' group
        admin_group, _ = Group.objects.get_or_create(name="Admin")
        user.groups.add(admin_group)

        return user


class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


class Profile(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHER = "O", "Other"

    class MaritalStatusChoices(models.TextChoices):
        SINGLE = "S", "Single"
        MARRIED = "M", "Married"

    class ProvincesChoices(models.TextChoices):
        KOSHI = "Koshi", "Koshi"
        MADHESH = "Madhesh", "Madhesh"
        BAGMATI = "Bagmati", "Bagmati"
        GANDAKI = "Gandaki", "Gandaki"
        LUMBINI = "Lumbini", "Lumbini"
        KARNALI = "Karnali", "Karnali"
        SUDURPASCHIM = "Sudurpaschim", "Sudurpaschim"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, unique=True)
    # need to pass null=True because of Profile instance creation by signals
    date_of_birth = models.DateField(null=True)
    address = models.CharField(max_length=100)
    avatar = models.ImageField(
        default="default_profile.jpg", upload_to="Users Avatars/"
    )
    gender = models.CharField(max_length=1, choices=GenderChoices.choices)
    marital_status = models.CharField(
        max_length=1,
        choices=MaritalStatusChoices.choices,
        default=MaritalStatusChoices.SINGLE,
    )
    post_code = models.CharField(max_length=10, default="44600")
    state = models.CharField(max_length=15, choices=ProvincesChoices.choices)
    city = models.CharField(max_length=50, blank=True, null=False, default="Kathmandu")
    country = models.CharField(max_length=100, default="Nepal")

    def __str__(self):
        return f"Profile: {self.user}"


def validate_id_length(value):
    if len(str(value)) < 6 or len(str(value)) > 10:
        raise ValidationError("ID must be between 6 and 10 digits.")


class StatusTextChoices(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"


class StudentManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .order_by("-created_at")
            .select_related("profile__user")
        )

    def total_students(self):
        self.get_queryset().count()

    def active_students(self):
        return self.filter(status=StatusTextChoices.ACTIVE)

    def inactive_students(self):
        return self.filter(status=StatusTextChoices.INACTIVE)


class Student(models.Model):
    class GuardianRelationChoices(models.TextChoices):
        FATHER = "FTH", "Father"
        MOTHER = "MTH", "Mother"
        GRANDFATHER = "GFA", "Grandfather"
        GRANDMOTHER = "GMO", "Grandmother"
        UNCLE = "UNC", "Uncle"
        AUNT = "AUN", "Aunt"
        BROTHER = "BRO", "Brother"
        SISTER = "SIS", "Sister"
        OTHER = "OTH", "Other"

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    student_id = models.PositiveIntegerField(
        unique=True, validators=[validate_id_length]
    )
    parent_contact = models.CharField(max_length=10, unique=True)
    guardian = models.CharField(max_length=100)
    guardian_relation = models.CharField(
        max_length=3,
        choices=GuardianRelationChoices.choices,
        default=GuardianRelationChoices.FATHER,
    )
    enrollment_date = models.DateField()
    graduation_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=StatusTextChoices.choices,
        default=StatusTextChoices.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = StudentManager()

    def __str__(self):
        return f"Student: {self.student_id}"

    def get_student_full_name(self):
        return self.profile.user.get_full_name()

    def get_enrolled_classes(self):
        return self.student_enrollments.all()


class QualificationChoices(models.TextChoices):
    # Academic Degrees
    PHD = "PHD", "PhD"
    MASTERS = "MASTERS", "Master's Degree"
    BACHELORS = "BACHELORS", "Bachelor's Degree"
    ASSOCIATE = "ASSOCIATE", "Associate Degree"


class InstructorManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .order_by("-created_at")
            .select_related("profile__user")
        )


class Instructor(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    employee_id = models.PositiveIntegerField(
        unique=True, validators=[validate_id_length]
    )
    qualification = models.CharField(
        max_length=20, choices=QualificationChoices.choices
    )
    date_of_joining = models.DateField()
    department = models.ForeignKey(
        "academics.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="instructors",
    )
    status = models.CharField(
        max_length=10,
        choices=StatusTextChoices.choices,
        default=StatusTextChoices.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = InstructorManager()

    def __str__(self):
        return f"Instructor: {self.profile.user.get_full_name()}"

    def get_instructor_full_name(self):
        return self.profile.user.get_full_name()
