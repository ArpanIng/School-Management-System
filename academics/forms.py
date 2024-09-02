from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout

from .models import AcademicYear, Department, Program, Semester
from .utils import ACTIVE_STATUS_CHOICES


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "code", "description", "head_of_department"]

    def clean_code(self):
        data = self.cleaned_data["code"]
        prefix = "DEP"
        if not data.startswith(prefix):
            raise forms.ValidationError("Department code must have 'DEP' prefix.")
        return data


class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        fields = ["year", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ["name", "start_date", "end_date", "academic_year", "status"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class ProgramForm(forms.ModelForm):
    """Form for the Program model."""

    class Meta:
        model = Program
        fields = [
            "code",
            "name",
            "department",
            "duration_years",
            "degree_type",
            "total_credits",
            "is_active",
        ]


class ProgramFilterForm(forms.Form):
    """Form for the filtering programs."""

    DEGREE_CHOICES = [("", "All")] + list(Program.DegreeType.choices)

    department = forms.ModelChoiceField(
        queryset=Department.objects.all(), label="Department:", required=False
    )
    degree_type = forms.ChoiceField(
        choices=DEGREE_CHOICES, label=" Degree type:", required=False
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
            Div("department", css_class="col-md-4"),
            Div("degree_type", css_class="col-md-4"),
            Div("is_active", css_class="col-md-4"),
        )
