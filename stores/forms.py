
from django import forms
from .models import Store

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'location', 'contact_number', 'email', 'address', 'image']
        widgets = {
            'image': forms.ClearableFileInput(),  
        }

