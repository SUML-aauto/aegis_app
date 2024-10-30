from django import forms
from .models import InsuranceForm


class InsuranceFormForm(forms.ModelForm):
    class Meta:
        model = InsuranceForm
        fields = '__all__'
