from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div

from .models import Class, Course, Enrollment
from academics.models import Program, Semester
from academics.utils import ACTIVE_STATUS_CHOICES
from users.models import Instructor, StatusTextChoices


class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["program"].queryset = Program.objects.filter(is_active=True)

    class Meta:
        model = Course
        fields = [
            "name",
            "code",
            "description",
            "credits",
            "program",
            "is_active",
        ]


class CourseFilterForm(forms.Form):
    program = forms.ModelChoiceField(
        queryset=Program.objects.all(),
        label="Progam:",
        required=False,
    )
    is_active = forms.ChoiceField(
        choices=ACTIVE_STATUS_CHOICES, label="Active status:", required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div("program", css_class="col-md-6"),
            Div("is_active", css_class="col-md-6"),
        )


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = "__all__"


class ClassForm(forms.ModelForm):
    """Form for the 'Class' model."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["course"].queryset = Course.objects.filter(is_active=True).only(
            "id", "name"
        )
        self.fields["semester"].queryset = Semester.objects.filter(
            status=Semester.SemesterStatus.ACTIVE
        )
        self.fields["class_instructor"].queryset = (
            Instructor.objects.filter(status=StatusTextChoices.ACTIVE)
            .select_related("profile__user")
            .only(
                "id",
                "profile__id",
                "profile__user__id",
                "profile__user__first_name",
                "profile__user__last_name",
            )
        )

    class Meta:
        model = Class
        fields = [
            "section",
            "course",
            "semester",
            "class_instructor",
            "max_students",
            "is_active",
        ]


class ClassFilterForm(forms.Form):
    pass


class ClassInstructorAssignForm(forms.ModelForm):
    """Form to assign instructor to a class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["class_instructor"].queryset = (
            Instructor.objects.filter(status=StatusTextChoices.ACTIVE)
            .select_related("profile__user")
            .only(
                "id",
                "profile__id",
                "profile__user__id",
                "profile__user__first_name",
                "profile__user__last_name",
            )
        )

    class Meta:
        model = Class
        fields = ["class_instructor"]
