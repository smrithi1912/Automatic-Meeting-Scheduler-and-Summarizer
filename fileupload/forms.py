from django import forms
from .models import Text

class TextForm(forms.ModelForm):
    title=forms.CharField()
    transcript=forms.CharField()
    class Meta:
        model=Text
        fields=[
        'title',
        'transcript',
        ]