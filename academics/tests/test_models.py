import datetime
from django.db import IntegrityError


from django.template.defaultfilters import slugify
from django.test import TestCase

from ..models import Department, AcademicYear, Semester


class DepartmentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.department = Department.objects.create(
            name="Management",
            code="DEP0001",
            description="lorem",
        )

    def test_name_max_length(self):
        field_label = self.department._meta.get_field("name").max_length
        self.assertEqual(field_label, 100)

    def test_code_max_length(self):
        field_label = self.department._meta.get_field("code").max_length
        self.assertEqual(field_label, 10)

    def test_object_representation(self):
        self.assertEqual(str(self.department), self.department.name)

    def test_department_has_slug(self):
        self.assertEqual(self.department.slug, slugify(self.department.name))


class AcademicYearModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.start_date = datetime.date(2023, 1, 1)
        cls.end_date = datetime.date(2024, 12, 31)
        cls.academic_year = AcademicYear.objects.create(
            year="2023-2024", start_date=cls.start_date, end_date=cls.end_date
        )

    def test_year_max_length(self):
        field_label = self.academic_year._meta.get_field("year").max_length
        self.assertEqual(field_label, 10)

    def test_object_representation(self):
        expected_str = f"{self.start_date.year} - {self.end_date.year}"
        self.assertEqual(str(self.academic_year), expected_str)


# class SemesterModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.start_date = datetime.date(2023, 1, 1)
#         cls.end_date = datetime.date(2024, 12, 31)
#         cls.academic_year = AcademicYear.objects.create(
#             name='Fall',
#             start_date=cls.start_date,
#             end_date=cls.end_date,
#             academic_year=sem
#         )
