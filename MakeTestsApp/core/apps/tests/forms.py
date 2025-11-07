from django import forms
from .models import Test, Question, Answer


class TestAdminForm(forms.ModelForm):
    max_tags = 4

    def clean(self):
        cleaned_data = super().clean()
        tags = cleaned_data.get('tag')
        if tags and tags.count() > self.max_tags:
            raise forms.ValidationError(
                f'Не больше {self.max_tags} тегов'
            )
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
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'questions-edit__add-question-form-input span-input',
                'placeholder': 'Новый вопрос'
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


class PostAnswersForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions', [])
        super().__init__(*args, **kwargs)

        for question in questions:
            answers = getattr(question, 'prefetched_answers', [])
            field_name = f"question_{question.id}"

            if question.type == 'SC':
                self.fields[field_name] = forms.ChoiceField(
                    choices=[(str(a.id), a.text) for a in answers],
                    widget=forms.RadioSelect(attrs={
                        'class': 'test-run__answer-radio'
                    }),
                    required=True,
                    label=question.text,
                )

            elif question.type == 'MC':
                self.fields[field_name] = forms.MultipleChoiceField(
                    choices=[(str(a.id), a.text) for a in answers],
                    widget=forms.CheckboxSelectMultiple(attrs={
                        'class': 'test-run__answer-checkbox'
                    }),
                    required=False,
                    label=question.text
                )

            elif question.type == 'TF':
                self.fields[field_name] = forms.CharField(
                    widget=forms.TextInput(attrs={
                        'class': 'test-run__answer-text-field',
                        'placeholder': 'Введите ответ',
                    }),
                    required=True,
                    label=question.text,
                )
