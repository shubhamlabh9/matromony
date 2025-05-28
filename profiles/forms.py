from django import forms
from .models import UserProfile, InterestRequest

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'date_of_birth', 'gender', 'religion', 'caste', 'mother_tongue',
            'marital_status', 'height', 'weight', 'occupation', 'education',
            'annual_income', 'location', 'bio', 'photo'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'religion': forms.TextInput(attrs={'class': 'form-control'}),
            'caste': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_tongue': forms.TextInput(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
            'height': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 5\'6"'}),
            'weight': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 65 kg'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'education': forms.TextInput(attrs={'class': 'form-control'}),
            'annual_income': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 5-10 Lakhs'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'photo': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class InterestRequestForm(forms.ModelForm):
    class Meta:
        model = InterestRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write a message to introduce yourself...'
            })
        }
