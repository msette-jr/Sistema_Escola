from django import forms
from .models import Aluno

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome']

class NotaForm(forms.Form):
    aluno = forms.ModelChoiceField(queryset=Aluno.objects.all(), label="Aluno")
    nota = forms.FloatField(label="Nota")
