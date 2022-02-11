from django import forms

from proofchecker.forms import ProofForm
from proofchecker.models import Assignment, Problem, Proof


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'course', 'due_by', 'problems']


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['question', 'grade']

    def __init__(self, *args, **kwargs):
        super(ProblemForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['onkeydown'] = 'replaceCharacter(this)'

