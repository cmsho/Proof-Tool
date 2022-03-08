from django import forms

from proofchecker.models import Assignment, Problem, Proof


class DateInput(forms.DateInput):
    input_type = 'date'


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'course', 'due_by']
        widgets = {
            'due_by': DateInput()
        }


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['question', 'point', 'target_steps']

    def __init__(self, *args, **kwargs):
        super(ProblemForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['onkeydown'] = 'replaceCharacter(this)'


class StudentProblemForm(ProblemForm):
    def __init__(self, *args, **kwargs):
        super(StudentProblemForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['question'].widget.attrs['disabled'] = 'disabled'
            self.fields['point'].widget.attrs['disabled'] = 'disabled'
            self.fields['target_steps'].widget.attrs['disabled'] = 'disabled'


class ProblemProofForm(forms.ModelForm):
    class Meta:
        model = Proof
        fields = ['rules', 'premises', 'conclusion']

    def __init__(self, *args, **kwargs):
        super(ProblemProofForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['onkeydown'] = 'replaceCharacter(this)'


class StudentProblemProofForm(ProblemProofForm):
    def __init__(self, *args, **kwargs):
        super(StudentProblemProofForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['rules'].widget.attrs['disabled'] = 'disabled'
            self.fields['premises'].widget.attrs['disabled'] = 'disabled'
            self.fields['conclusion'].widget.attrs['disabled'] = 'disabled'
