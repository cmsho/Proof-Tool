from django import forms

from .models import Proof, ProofLine


class ProofForm(forms.ModelForm):
    class Meta:
        model = Proof
        fields = ['name', 'premises', 'conclusion']

    def __init__(self, *args, **kwargs):
        super(ProofForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['onkeydown'] = 'replaceCharacter(this)'


class ProofCheckerForm(forms.ModelForm):
    class Meta:
        model = ProofLine
        fields = ['line_no', 'formula', 'rule']

    def __init__(self, *args, **kwargs):
        super(ProofCheckerForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['onkeydown'] = 'replaceCharacter(this)'


class ProofLineForm(forms.ModelForm):
    class Meta:
        model = ProofLine
        fields = ['ORDER', 'line_no', 'formula', 'rule']

    def __init__(self, *args, **kwargs):
        super(ProofLineForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['onkeydown'] = 'replaceCharacter(this)'
