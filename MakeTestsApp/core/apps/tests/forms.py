from django import forms
from .models import Test


class TestAdminForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        tags = cleaned_data.get('tag')
        if tags and tags.count() > 4:
            raise forms.ValidationError('Вы можете выбрать не более 4 тегов.')
        return cleaned_data

class AddTestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'create-test-container__form-field-input span-text',
                    'placeholder': 'Название теста',
                    'autocomplete': 'off'
                }
            ),
        }

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if len(title) < 3:
            raise forms.ValidationError("Название должно быть не короче 3 символов.")
        return title
