from django import forms

from academics.models import Program, Semester
from users.models import Instructor, StatusTextChoices

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div

from .models import Class, Course, Enrollment


class TestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    class Meta:
        model = Course
        fields = "__all__"


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
    program = forms.ModelMultipleChoiceField(queryset=Program.objects.all(), widget=forms.CheckboxSelectMultiple,required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div("program", css_class="col-md-6"),
        )
    
    
    # ACTIVE_STATUS_CHOICES = (
    #     ("", "All"),
    #     ("1", "Yes"),
    #     ("0", "No"),
    # )
    # ORDER_BY_STATUS_CHOICES = ()
    # is_active = forms.ChoiceField(required=False, choices=ACTIVE_STATUS_CHOICES)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_method = "get"
    #     self.helper.form_class = "row row-cols-lg-auto g-3 align-items-center"
    #     self.helper.layout = Layout(
    #         Row(
    #             Column(
    #                 Field("is_active", wrapper_class="input-group"), css_class="col-12"
    #             ),
    #             css_class="form-row",
    #         )
    #     )


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
