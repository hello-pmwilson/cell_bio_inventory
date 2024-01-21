from django import forms
from .models import on_request, inventory, item, unit, location

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

class unitForm(forms.ModelForm):
    class Meta:
        model = unit
        fields = "__all__"

class locationForm(forms.ModelForm):
    class Meta:
        model = location
        fields = "__all__"