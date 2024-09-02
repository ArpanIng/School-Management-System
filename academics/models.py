from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify

from users.models import Instructor


class Department(models.Model):
    """
    Model to represent an academic department.
    """

    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True, help_text="Use 'DEP' prefix.")
    description = models.TextField()
    head_of_department = models.OneToOneField(
        Instructor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="department_head",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class AcademicYear(models.Model):
    """
    Model to represent an academic year.
    """

    year = models.CharField(
        max_length=10, help_text="Enter the academic year in the format 'YYYY-YYYY'"
    )
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["start_date", "end_date"], name="unique_academic_year_dates"
            )
        ]

    def __str__(self):
        return f"{self.start_date.year} - {self.end_date.year}"


class Semester(models.Model):
    class SemesterChoices(models.TextChoices):
        FALL = "FALL", "Fall"
        SPRING = "SPRING", "Spring"
        SUMMER = "SUMMER", "Summer"
        WINTER = "WINTER", "Winter"

    class SemesterStatus(models.TextChoices):
        ACTIVE = "ACT", "Active"
        COMPLETED = "COMP", "Completed"
        ARCHIVED = "ARC", "Archived"

    name = models.CharField(max_length=10, choices=SemesterChoices.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    academic_year = models.ForeignKey(
        AcademicYear, on_delete=models.CASCADE, related_name="semesters"
    )
    status = models.CharField(
        max_length=5,
        choices=SemesterStatus.choices,
        default=SemesterStatus.ACTIVE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "start_date", "end_date", "academic_year"],
                name="unique_semester",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.start_date} - {self.end_date})"


class Program(models.Model):
    """
    Model to represent an academic program offered by a department.
    """

    class DegreeType(models.TextChoices):
        BSC = "B.Sc.", "Bachelor of Science"
        BA = "B.A.", "Bachelor of Arts"
        BENG = "B.Eng.", "Bachelor of Engineering"

        MSC = "M.Sc.", "Master of Science"
        MA = "M.A.", "Master of Arts"
        MENG = "M.Eng.", "Master of Engineering"

        MBA = "MBA", "Master of Business Administration"
        BBA = "BBA", "Bachelor of Business Administration"

    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True, help_text="USE 'PROG' prefix.")
    description = models.TextField()
    department = models.ForeignKey(
        Department, on_delete=models.RESTRICT, related_name="programs"
    )
    duration_years = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        help_text="Enter the number of years required to complete this program.",
    )
    degree_type = models.CharField(max_length=10, choices=DegreeType.choices)
    total_credits = models.PositiveIntegerField(validators=[MaxValueValidator(300)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
