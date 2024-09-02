from django.db import models
from django.utils import timezone

from courses.models import Class
from users.models import Student


class AttendanceManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .order_by("-created_at")
            .select_related("course_class", "student__profile__user")
        )


class Attendance(models.Model):
    class AttendanceStatus(models.TextChoices):
        PRESENT = "PRE", "Present"
        ABSENT = "ABS", "Absent"

    course_class = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name="attendances"
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="attendances"
    )
    attendance_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=3, choices=AttendanceStatus.choices)
    remarks = models.CharField(max_length=255, null=False, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AttendanceManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["course_class", "student", "attendance_date"],
                name="unique_attendance_per_student_per_class_per_date",
            )
        ]
        indexes = [models.Index(fields=["attendance_date", "course_class"])]
        ordering = ["attendance_date", "course_class"]
