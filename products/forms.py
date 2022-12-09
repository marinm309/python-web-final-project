from django import forms
from . models import ShippingAddress

class ShippingForm(forms.ModelForm):
    name = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(required=False)
    class Meta:
        model = ShippingAddress
        fields = ['country', 'city', 'zip', 'address']