from django import forms
from django.forms import TextInput
from .models import on_request, inventory, item, unit, location

class onRequestForm(forms.ModelForm):
    item_char = forms.CharField(max_length=100, required=False)

    class Meta:
        model = on_request
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(onRequestForm, self).__init__(*args, **kwargs)
        self.fields['item_char'].widget = TextInput(attrs={'id': 'item_char_field', 'list': 'itemOptions'})

class inventoryAddForm(forms.ModelForm):
    item_char = forms.CharField(max_length=100, required=False)

    class Meta:
        model = inventory
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super(inventoryAddForm, self).__init__(*args, **kwargs)
        self.fields['item_char'].widget = TextInput(attrs={'id': 'item_char_field', 'list': 'itemOptions'})

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