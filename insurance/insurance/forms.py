from django import forms
from .models import InsuranceForm

# Existing ModelForm
class InsuranceFormForm(forms.ModelForm):
    class Meta:
        model = InsuranceForm
        fields = '__all__'

        widgets = {
            'gender': forms.RadioSelect(),
            'marital_status': forms.RadioSelect(),
            'employment': forms.RadioSelect(),
        }

# New SupportForm for the Support feature
class SupportForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Your Name")
    email = forms.EmailField(required=True, label="Your Email")
    message = forms.CharField(widget=forms.Textarea, required=True, label="Your Message")
