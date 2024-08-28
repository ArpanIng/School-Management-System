from django import forms

from .models import AcademicYear, Department, Program, Semester


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
        fields = "__all__"
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ["name", "start_date", "end_date", "academic_year"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = "__all__"
        exclude = ["slug"]
