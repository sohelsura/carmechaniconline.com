from django import forms
from main.models import ProductEnquiry

class ProductEnquiryForm(forms.ModelForm):
    class Meta:
        model = ProductEnquiry
        fields = ['name', 'email', 'contact', 'message']