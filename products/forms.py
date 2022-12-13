from django import forms
from . models import ShippingAddress, Products

class ShippingForm(forms.ModelForm):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'hide'})
        self.fields['email'].widget.attrs.update({'class': 'hide'})

    class Meta:
        model = ShippingAddress
        fields = ['country', 'city', 'zip', 'address']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if 'img' in field:
                continue
            self.fields[field].widget.attrs.update({"autocomplete": "current-password", 'class': 'form-control form-control-lg'})