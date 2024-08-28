import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from ..models import Department, AcademicYear, Semester


class DepartmentListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            email="john@example.com",
            username="john",
            password="superadmin",
        )
        cls.admin_group, _ = Group.objects.get_or_create(name="Admin")

        # cls.department = Department.objects.create()

    def setUp(self):
        self.client.login(email="john@example.com", password="superadmin")
        self.url_name = reverse("academics:department_list")

    def test_admin_user_access(self):
        # Assign user to Admin group
        self.user.groups.add(self.admin_group)
        response = self.client.get(self.url_name)
        self.assertEqual(response.status_code, 200)

    def test_non_admin_user_access(self):
        # Log the user in without assigning them to the Admin group
        response = self.client.get(self.url_name)
        self.assertEqual(response.status_code, 403)

    def test_view_url_exists_at_correct_location(self):
        self.user.groups.add(self.admin_group)
        response = self.client.get("/departments/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessable_by_name(self):
        self.user.groups.add(self.admin_group)
        response = self.client.get(self.url_name)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.user.groups.add(self.admin_group)
        response = self.client.get(self.url_name)
        self.assertTemplateUsed(response, "academics/departments/department_list.html")

    def test_view_for_logged_out_user(self):
        # logout the user and check access
        self.client.logout()
        response = self.client.get(self.url_name)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url_name}")


class AcademicYearListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            email="john@example.com",
            username="john",
            password="superadmin",
        )
        cls.admin_group, _ = Group.objects.get_or_create(name="Admin")
        cls.academic_years = [
            AcademicYear.objects.create(
                start_date=datetime.date(2024, 1, 1),
                end_date=datetime.date(2024, 12, 31),
            ),
            AcademicYear.objects.create(
                start_date=datetime.date(2023, 1, 1),
                end_date=datetime.date(2023, 12, 31),
            ),
        ]
        # cls.academic_year = AcademicYear.objects.create(
        #     year="2023-2024", start_date=datetime.date(2024, 1, 1), end_date=datetime.date(2024, 12, 31),
        # )

    def setUp(self):
        self.client.login(email="john@example.com", password="superadmin")
        self.url = reverse("academics:academicyear_list")

    def test_total_academicyears_in_context(self):
        self.user.groups.add(self.admin_group)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.context['total_academicyears'], len(self.academic_year))


class SemesterListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            email="john@example.com",
            username="john",
            password="superadmin",
        )
        cls.admin_group, _ = Group.objects.get_or_create(name="Admin")

    def setUp(self):
        self.client.login(email="john@example.com", password="superadmin")
        self.url = reverse("academics:semester_list")

    def test_total_semester_in_context(self):
        self.user.groups.add(self.admin_group)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
