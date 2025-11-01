from django import forms
from .models import Test, Question, Answer


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


class TestEditForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'test-info-edit__title-input span-title',
                'autocomplete': 'off',
                'placeholder': 'Введите название теста'
            }),
            'content': forms.Textarea(attrs={
                'class': 'test-info-edit__content-textarea span-input',
                'placeholder': 'Описание теста'
            }),
        }


class AddQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'type']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'questions-edit__add-question-form-input span-input',
                'placeholder': 'Новый вопрос'
            }),
            'type': forms.Select(attrs={
                'class': 'questions-edit__type-selector'
            }),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'flag']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'questions-edit__answer-input span-answer-input',
                'placeholder': 'Новый ответ'
            }),
        }
