from django import forms
from .models import InsuranceForm

class InsuranceFormForm(forms.ModelForm):
    class Meta:
        model = InsuranceForm
        fields = '__all__'

        widgets = {
            'gender': forms.RadioSelect(),
            'marital_status': forms.RadioSelect(),
            'employment': forms.RadioSelect(),
        }
