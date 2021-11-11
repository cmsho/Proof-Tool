from django import forms

from .models import Proof, ProofLine, Assignment


class ProofForm(forms.ModelForm):
    class Meta:
        model = Proof
        fields = ['premise', 'conclusion']

# class ProofForm(forms.Form):
#     premise = forms.CharField(max_length=255)
#     conclusion = forms.CharField(max_length=255)
#
#     def clean(self):
#         cleaned_data = self.cleaned_data
#         return cleaned_data

class ProofLineForm(forms.ModelForm):
    class Meta:
        model = ProofLine
        fields = ['line_no', 'formula', 'rule']


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'due_by', 'problems', 'course']
