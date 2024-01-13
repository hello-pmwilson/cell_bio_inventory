from django import forms
from .models import on_request, inventory, item

class onRequestForm(forms.ModelForm):
    class Meta:
        model = on_request
        fields = "__all__"

class inventoryAddForm(forms.ModelForm):
    class Meta:
        model = inventory
        fields = "__all__"

class itemAddForm(forms.ModelForm):
    class Meta:
        model = item
        fields = "__all__"