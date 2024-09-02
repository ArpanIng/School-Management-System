from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout

from academics.models import Department
from .models import (
    Instructor,
    Profile,
    Student,
    QualificationChoices,
    StatusTextChoices,
)


class RegistrationForm(UserCreationForm):
    """Form for creating/registring new user."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div("first_name", css_class="col-md-6"),
            Div("last_name", css_class="col-md-6"),
            Div("username", css_class="col-md-6"),
            Div("email", css_class="col-md-6"),
            Div("password1", css_class="col-md-12"),
            Div("password2", css_class="col-md-12"),
        )
        self.fields["password1"].help_text = None

    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "username", "email"]
        help_texts = {
            "username": None,
        }


class MyUserChangeForm(UserChangeForm):
    """Form for updating user."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div("first_name", css_class="col-md-6"),
                Div("last_name", css_class="col-md-6"),
                Div("username", css_class="col-md-6"),
                Div("email", css_class="col-md-6"),
                Div("password", css_class="col-md-12"),
                css_class="row g-3",
            )
        )
        user = self.instance
        password_change_url = reverse(
            "admin_password_change", kwargs={"user_id": user.id}
        )
        self.fields["password"].help_text = (
            "Raw passwords are not stored, so there is no way to see this "
            "user’s password, but you can change the password using "
            f'<a href="{password_change_url}">this form</a>.'
        )

    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "username", "email", "password"]
        help_texts = {
            "username": None,
        }


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields["password"].disabled = True
        self.fields["date_joined"].disabled = True
        self.fields["last_login"].disabled = True

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "date_joined",
            "last_login",
        ]


class ProfileForm(forms.ModelForm):
    """Form for the Profile model."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div("avatar", css_class="col-md-12"),
            Div("gender", css_class="col-md-4"),
            Div("date_of_birth", css_class="col-md-4"),
            Div("marital_status", css_class="col-md-4"),
            Div("phone_number", css_class="col-md-6"),
            Div("address", css_class="col-md-6"),
            Div("city", css_class="col-md-6"),
            Div("state", css_class="col-md-2"),
            Div("post_code", css_class="col-md-2"),
            Div("country", css_class="col-md-2"),
        )

    class Meta:
        model = Profile
        fields = [
            "avatar",
            "gender",
            "date_of_birth",
            "marital_status",
            "phone_number",
            "address",
            "city",
            "state",
            "post_code",
            "country",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "phone_number": forms.NumberInput(attrs={"type": "tel"}),
        }


class StudentForm(forms.ModelForm):
    """Form for the Student model."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div("student_id", css_class="col-md-12"),
            Div("parent_contact", css_class="col-md-4"),
            Div("guardian", css_class="col-md-4"),
            Div("guardian_relation", css_class="col-md-4"),
            Div("enrollment_date", css_class="col-md-4"),
            Div("graduation_date", css_class="col-md-4"),
            Div("status", css_class="col-md-4"),
        )

    class Meta:
        model = Student
        fields = [
            "student_id",
            "parent_contact",
            "guardian",
            "guardian_relation",
            "enrollment_date",
            "graduation_date",
            "status",
        ]
        widgets = {
            "parent_contact": forms.NumberInput(
                attrs={"type": "tel", "pattern": "[0-9]*"}
            ),
            "enrollment_date": forms.DateInput(attrs={"type": "date"}),
            "graduation_date": forms.DateInput(attrs={"type": "date"}),
        }
        help_texts = {
            "student_id": "Enter a unique Student ID between 6 and 10 digits long.",
            "guardian": "Enter the full name of the student's guardian",
        }


class StudentFilterForm(forms.Form):
    """Form for filtering students."""

    PROVINCE_CHOICES = [("", "All")] + Profile.ProvincesChoices.choices
    MARITAL_STATUS = [("", "All")] + list(Profile.MaritalStatusChoices.choices)
    GENDER_CHOICES = [("", "All")] + list(Profile.GenderChoices.choices)
    STATUS_CHOICES = [("", "All")] + list(StatusTextChoices.choices)

    state = forms.ChoiceField(
        choices=PROVINCE_CHOICES, label="Province:", required=False
    )
    marital_status = forms.ChoiceField(
        choices=MARITAL_STATUS, label=" Marital status:", required=False
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label="Gender:", required=False)
    status = forms.ChoiceField(choices=STATUS_CHOICES, label="Status:", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Div("state", css_class="col-md-3"),
            Div("marital_status", css_class="col-md-3"),
            Div("gender", css_class="col-md-3"),
            Div("status", css_class="col-md-3"),
        )


class InstructorForm(forms.ModelForm):
    """Form for the Instructor model."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div("employee_id", css_class="col-md-12"),
            Div("qualification", css_class="col-md-6"),
            Div("date_of_joining", css_class="col-md-6"),
            Div("department", css_class="col-md-6"),
            Div("status", css_class="col-md-6"),
        )

    class Meta:
        model = Instructor
        fields = [
            "employee_id",
            "qualification",
            "date_of_joining",
            "department",
            "status",
        ]
        widgets = {
            "date_of_joining": forms.DateInput(attrs={"type": "date"}),
        }
        help_texts = {
            "employee_id": "Enter a unique Instructor ID between 6 and 10 digits long.",
            "guardian": "Enter the full name of the student's guardian",
        }


class InstructorFilterForm(forms.Form):
    """Form for filtering instructors."""

    QUALIFICATION_CHOICES = [("", "All")] + list(QualificationChoices.choices)
    PROVINCE_CHOICES = [("", "All")] + Profile.ProvincesChoices.choices
    MARITAL_STATUS = [("", "All")] + list(Profile.MaritalStatusChoices.choices)
    GENDER_CHOICES = [("", "All")] + list(Profile.GenderChoices.choices)
    STATUS_CHOICES = [("", "All")] + list(StatusTextChoices.choices)

    qualification = forms.ChoiceField(
        choices=QUALIFICATION_CHOICES, label="Qualification:", required=False
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        label="Department:",
        required=False,
    )
    state = forms.ChoiceField(
        choices=PROVINCE_CHOICES, label="Province:", required=False
    )
    marital_status = forms.ChoiceField(
        choices=MARITAL_STATUS, label=" Marital status:", required=False
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label="Gender:", required=False)
    status = forms.ChoiceField(choices=STATUS_CHOICES, label="Status:", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Div("qualification", css_class="col-md-2"),
            Div("department", css_class="col-md-2"),
            Div("state", css_class="col-md-2"),
            Div("marital_status", css_class="col-md-2"),
            Div("gender", css_class="col-md-2"),
            Div("status", css_class="col-md-2"),
        )
