from django import forms
from .models import Profile, ChatRequest

class ProfileForm(forms.ModelForm):
    LEARNING_INTEREST_CHOICES = Profile.LEARNING_INTEREST_CHOICES

    learning_interest = forms.MultipleChoiceField(
        choices=LEARNING_INTEREST_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Profile
        fields = ['avatar', 'firstname', 'lastname', 'bio', 'location', 'age', 'gender', 'learning_interest']
        labels = {
            'firstname': 'First Name',
            'lastname': 'Last Name',
            'bio': 'Bio',
            'location': 'Location',
            'age': 'Age',
            'gender': 'Gender',
            'learning_interest': 'Learning Interest',
            'avatar': 'Avatar'
        }
        widgets = {
            'avatar': forms.TextInput(attrs={
                'onchange': "previewProfileImage(event)",
                "type": "file",
                "id": "profileImageInput",
                "accept": "image/*",
                "style":"display:none"
            }),
            'gender': forms.Select(choices=Profile.GENDER_CHOICES , attrs={"class": "bg-white focus:outline-none border border-gray-300 rounded-lg py-2 px-4 block w-full appearance-none leading-normal text-gray-700"}),
            "firstname": forms.TextInput(attrs={
                "class": "textinput leading-normal py-2 appearance-none block rounded-lg text-gray-700 w-full border-gray-300 bg-white border px-4 focus:outline-none"
            }),
            "lastname": forms.TextInput(attrs={
                "class": "textinput leading-normal py-2 appearance-none block rounded-lg text-gray-700 w-full border-gray-300 bg-white border px-4 focus:outline-none"
            }),
            "bio": forms.TextInput(attrs={
                "class": "textarea leading-normal py-2 appearance-none block rounded-lg text-gray-700 w-full border-gray-300 bg-white border px-4 focus:outline-none",
                "cols":"40" , "rows":"10"}),
            
            "location": forms.TextInput(attrs={
                "class": "textinput leading-normal py-2 appearance-none block rounded-lg text-gray-700 w-full border-gray-300 bg-white border px-4 focus:outline-none",
            }),
            "age": forms.TextInput(attrs={
                "class": "numberinput leading-normal py-2 appearance-none block rounded-lg text-gray-700 w-full border-gray-300 bg-white border px-4 focus:outline-none",
                "type":"number"
            }),
            
        }
        
        def clean_age(self):
            age = self.cleaned_data.get('age')
            if age is not None and (age < 0 or age > 100):
                raise forms.ValidationError("Age must be between 0 and 100.")
            return age

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.learning_interest:
            self.fields['learning_interest'].initial = self.instance.learning_interest

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.learning_interest = self.cleaned_data['learning_interest']
        if commit:
            instance.save()
        return instance


class ChatRequestForm(forms.ModelForm):
    class Meta:
        model = ChatRequest
        fields = ['to_user', 'message']


class RatingForm(forms.Form):
    score = forms.IntegerField(
        label='Score', min_value=1, max_value=5,
        widget=forms.NumberInput(attrs={
            'type': 'number',
            "id": "score_input",
            "value": "1",
            "style": "display:none"
        })
    )
    comment = forms.CharField(
        label='Comment', required=False,
        widget=forms.Textarea(attrs={
            'rows': 6,
            "class": "w-full p-3 feedback-textarea flex-grow",
            "placeholder": "Start typing...",
            'id':"feedback-text"
        })
    )
