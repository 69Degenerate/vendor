from django import forms
from .models import CompanyData

class CompanyDataForm(forms.ModelForm):
    class Meta:
        model = CompanyData
        fields = ['company_name', 'company_address', 'company_logo', 'company_stamp']
