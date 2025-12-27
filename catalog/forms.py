from django import forms
from .models import ProductType

class NewProductForm(forms.Form):
    # name = forms.CharField(max_length=200, label='Product Name')
    product_type = forms.ModelChoiceField(widget=forms.RadioSelect, queryset=ProductType.objects.all(), label='Product Type')