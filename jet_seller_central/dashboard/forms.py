from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Product
from .helper_functions import ProductAPI

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = []