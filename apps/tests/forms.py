from django import forms

from .models import Test


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
