from django import forms

from .models import Proof, ProofLine, Assignment


class ProofForm(forms.ModelForm):
    class Meta:
        model = Proof
        fields = ['premises', 'conclusion']

    def __init__(self, *args, **kwargs):
        super(ProofForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'text-replacement-enabled'

class ProofLineForm(forms.ModelForm):
    class Meta:
        model = ProofLine
        fields = ['line_no', 'formula', 'rule']

    def __init__(self, *args, **kwargs):
        super(ProofLineForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'text-replacement-enabled'


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'due_by', 'problems', 'course']
