from django import forms
from .models import Proof

class ProofForm(forms.ModelForm):
    class Meta:
        model = Proof
        fields = "__all__"