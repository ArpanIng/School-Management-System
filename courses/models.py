from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from academics.models import Program, Semester
from users.models import Instructor, Student


class Course(models.Model):
    """
    Model to represent a course for an academic progam.
    """

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True, help_text="USE 'COU' prefix.")
    description = models.TextField()
    credits = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    program = models.ForeignKey(
        Program, on_delete=models.RESTRICT, related_name="courses"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["slug"], name="slug_idx")]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "program"], name="unique_course_in_program"
            )
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("courses:course_detail", kwargs={"course_slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Class(models.Model):
    section = models.CharField(max_length=10, help_text="e.g., Section A, B, 01, 02")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="classes")
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, related_name="classes"
    )
    class_instructor = models.ForeignKey(
        Instructor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="classes",
    )
    students = models.ManyToManyField(Student, through="Enrollment")
    max_students = models.IntegerField(
        default=100,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Maximum number of students allowed in the class.",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["section", "course"], name="unique_section_course"
            )
        ]
        verbose_name = "Class"
        verbose_name_plural = "Classes"

    def __str__(self):
        return f"{self.section}"

    def get_absolute_url(self):
        return reverse("courses:class_detail", kwargs={"class_id": self.id})

    def get_enrolled_students(self):
        """Get all enrolled students of a course."""
        return (
            self.students.all()
            .select_related("profile__user")
            .order_by("profile__user__first_name")
        )

    def is_enrolled(self, student):
        """Check if a user/student is enrolled in a course."""
        return self.students.filter(profile__user=student).exists()

    def get_class_instructor_full_name(self):
        return self.class_instructor.profile.user.get_full_name()


class Enrollment(models.Model):
    class EnrollmentStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        DROPPED = "DROPPED", "Dropped"

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="student_enrollments"
    )
    class_instance = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name="class_enrollments"
    )
    status = models.CharField(
        max_length=10,
        choices=EnrollmentStatus.choices,
        default=EnrollmentStatus.ACTIVE,
    )
    enrollment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "class_instance"],
                name="unique_student_class_enrollment",
            )
        ]

    def __str__(self):
        return f"Enrollment: {self.id}"


class Assessment(models.Model):
    class AssessmentChoices(models.TextChoices):
        CONTINUOUS = "CONTINUOUS", "Continuous Assessment"
        FINAL = "FINAL", "Final Assessment"

    title = models.CharField(max_length=255)
    description = models.TextField(null=False, blank=True, max_length=1000, default="")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="course_assessments"
    )
    associated_class = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name="class_assessments"
    )
    type = models.CharField(max_length=20, choices=AssessmentChoices.choices)
    weightage = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    mark = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)]
    )
    remark = models.TextField(null=False, blank=True, max_length=1000, default="")
    due_date = models.DateTimeField()
    is_mandatory = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "course", "associated_class"],
                name="unique_assessment_course_class",
            ),
        ]

    def __str__(self):
        return f"{self.title} - {self.course.name} ({self.associated_class})"
