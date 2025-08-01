# forms.py

from django import forms
from .models import PartnerProfile

class PartnerProfileForm(forms.ModelForm):
    class Meta:
        model = PartnerProfile
        fields = [
            'biography',
            'native_language',
            'english_level',
            'learning_goals',
            'availability',
            'appear_in_search',
        ]
        widgets = {
            'biography': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'native_language': forms.TextInput(attrs={'class': 'form-control'}),
            'english_level': forms.Select(attrs={'class': 'form-select'}),
            'learning_goals': forms.Select(attrs={'class': 'form-select'}),
            'availability': forms.Select(attrs={'class': 'form-select'}),
            'appear_in_search': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
