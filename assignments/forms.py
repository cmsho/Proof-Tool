from django import forms
from proofchecker.models import Assignment, Problem


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'course', 'due_by', 'problems']
