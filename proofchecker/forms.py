from django import forms

from .models import Proof, ProofLine, Assignment


class ProofForm(forms.ModelForm):
    class Meta:
        model = Proof
        fields = ['premises', 'conclusion']

class ProofLineForm(forms.ModelForm):
    class Meta:
        model = ProofLine
        fields = ['line_no', 'formula', 'rule']


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'due_by', 'problems', 'course']
