from django import forms

from .models.answer import Answer
from .models.question import Question
from .models.test import Test


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


class TestContentForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'test-info-edit__content-textarea span-input',
                'placeholder': 'Описание теста'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].required = False


class TestTitleForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'test-info-edit__title-input span-title',
                'autocomplete': 'off',
                'placeholder': 'Введите название теста'
            }),
        }


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'questions-edit__add-question-form-input span-input',
                'placeholder': 'Новый вопрос'
            }),
        }


class AnswerCreateForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'flag']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'questions-edit__answer-input span-answer-input',
                'placeholder': 'Новый ответ'
            }),
        }
