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


class QuestionForm(forms.ModelForm):
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


class TagForm(forms.Form):
    tag_id = forms.IntegerField()


class QuestionTypeForm(forms.Form):
    type = forms.ChoiceField(
        choices=Question.QuestionType.choices,
        required=True
    )


class AnswerTextForm(forms.Form):
    text = forms.CharField()


class AnswerFlagForm(forms.Form):
    flag = forms.BooleanField(required=False)


class UploadImageForm(forms.Form):
    image = forms.ImageField(required=True)


class PostAnswersForm(forms.Form):

    def __init__(self, *args, questions, **kwargs):
        super().__init__(*args, **kwargs)

        for question in questions:
            field_name = str(question.id)
            answers = question.answers.all()

            if question.type == Question.QuestionType.SINGLE_CHOICE:
                self.fields[field_name] = forms.ChoiceField(
                    choices=[
                        (str(answer.id), answer.text)
                        for answer in answers
                    ],
                    widget=forms.RadioSelect(attrs={
                        'class': 'test-run__answer-radio',
                    }),
                    required=True,
                    label=question.text,
                )

            elif question.type == Question.QuestionType.MULTIPLE_CHOICES:
                self.fields[field_name] = forms.MultipleChoiceField(
                    choices=[
                        (str(answer.id), answer.text)
                        for answer in answers
                    ],
                    widget=forms.CheckboxSelectMultiple(attrs={
                        'class': 'test-run__answer-checkbox',
                    }),
                    required=False,
                    label=question.text,
                )

            elif question.type == Question.QuestionType.TEXT_FIELD:
                self.fields[field_name] = forms.CharField(
                    widget=forms.TextInput(attrs={
                        'class': 'test-run__answer-text-field',
                        'placeholder': 'Введите ответ',
                    }),
                    required=True,
                    label=question.text,
                )
