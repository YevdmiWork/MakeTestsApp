from django import forms
from .models import Test


class TestAdminForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        tags = cleaned_data.get('tag')
        if tags and tags.count() > 4:
            raise forms.ValidationError('Вы можете выбрать не более 4 тегов.')
        return cleaned_data
