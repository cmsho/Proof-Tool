from django import forms

from proofchecker.models import Assignment, Problem, Proof


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'course', 'due_by', 'problems']


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['question', 'point', 'target_steps']

    def __init__(self, *args, **kwargs):
        super(ProblemForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['onkeydown'] = 'replaceCharacter(this)'


class ProblemProofForm(forms.ModelForm):
    class Meta:
        model = Proof
        fields = ['rules', 'premises', 'conclusion']

    def __init__(self, *args, **kwargs):
        super(ProblemProofForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['onkeydown'] = 'replaceCharacter(this)'
