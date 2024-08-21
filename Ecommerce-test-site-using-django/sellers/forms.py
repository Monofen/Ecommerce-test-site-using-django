from django import forms
from .models import Sellers

class SellerForm(forms.ModelForm):
    class Meta:
        model = Sellers
        fields = [
            'name', 
            'khalti_api_code', 
            'citizenship', 
            'cit_num', 
            'owner_pic', 
            'registration_certificate', 
            'pan_number', 
            'pan_pic', 
            'facebook', 
            'instagram', 
            'youtube', 
            'extra'
        ]
        widgets = {
            'citizenship': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'owner_pic': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'registration_certificate': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'pan_pic': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make all fields required except for 'facebook', 'instagram', 'youtube', and 'extra'
        for field_name in self.fields:
            if field_name not in ['facebook', 'instagram', 'youtube', 'extra']:
                self.fields[field_name].required = True
