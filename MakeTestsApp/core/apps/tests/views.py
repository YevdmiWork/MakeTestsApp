from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView

from .forms import AddTestForm, TestEditForm, AddQuestionForm, AnswerForm, PostAnswersForm
from .models import Test, Question, Answer
from .services import create_test


class AllTests(ListView):
    template_name = "tests/tests_all.html"
    context_object_name = "tests"

    def get_queryset(self):
        return Test.published.all()


class BaseTestView(DetailView):
    slug_url_kwarg = 'test_slug'
    context_object_name = 'tests'


class TestView(BaseTestView):
    template_name = 'tests/test_view.html'

    def get_queryset(self):
        return Test.objects.with_test_content().with_test_data()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        test = self.object
        context['similar_tests'] = Test.objects.similar_to(test)
        return context


class TestRun(BaseTestView):
    template_name = 'tests/test_run.html'
    form_class = PostAnswersForm

    def get_queryset(self):
        return Test.objects.with_fields()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        test = self.object
        questions = Question.objects.for_test(test)
        form = self.form_class(questions=questions)
        question_fields = []
        for i, question in enumerate(questions):
            field_name = f"question_{question.id}"
            field = form[field_name]
            question_fields.append((question, field))

        context['question_fields'] = question_fields
        return context


class AddTest(LoginRequiredMixin, CreateView):
    model = Test
    template_name = 'tests/add_test.html'
    form_class = AddTestForm

    def form_valid(self, form):
        test = create_test(self.request.user, form.cleaned_data)
        return redirect(test.get_edit_url())


class TestEdit(BaseTestView):
    model = Test
    context_object_name = 'test'
    template_name = 'tests/test_edit.html'

    def get_queryset(self):
        return Test.objects.with_test_status().with_test_content()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test_edit_form'] = TestEditForm(instance=self.object)
        context['add_question_form'] = AddQuestionForm()
        context['add_answer_form'] = AnswerForm()
        context['questions'] = Question.objects.with_answers().filter(test=self.object)
        context['type_of_question_choices'] = Question.QuestionType.choices
        return context


@require_POST
def update_test_info(request):
    test_id = request.POST.get('test_id')
    title = request.POST.get('title')
    content = request.POST.get('content')

    if not test_id:
        return JsonResponse({'success': False, 'error': 'Не указан ID теста'})

    try:
        test = Test.objects.get(pk=test_id, author=request.user)
    except Test.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Тест не найден или нет прав'})

    if title is not None:
        test.title = title
    if content is not None:
        test.content = content

    test.save(update_fields=['title', 'content', 'time_update'])

    return JsonResponse({'success': True, 'message': 'Изменения сохранены'})


@require_POST
def add_question(request):
    test_id = request.POST.get('test_id')
    text = request.POST.get('text')

    if not test_id or not text:
        return JsonResponse({'success': False, 'error': 'Не указаны обязательные поля'})

    try:
        test = Test.objects.get(pk=test_id, author=request.user)
    except Test.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Тест не найден или нет прав'})

    default_type = Question.QuestionType.SINGLE_CHOICE
    question = Question.objects.create(test=test, text=text, type=default_type)

    question_number = test.related_test.count()

    question_html = render_to_string('tests/question_block.html', {
        'question': question,
        'question_number': question_number,
        'type_of_question_choices': Question.QuestionType.choices,
        'add_answer_form': AnswerForm(),
    }, request=request)

    return JsonResponse({'success': True, 'question_html': question_html})


@require_POST
def update_answer(request):
    answer_id = request.POST.get('answer_id')
    text = request.POST.get('text')
    flag = request.POST.get('flag')

    if not answer_id:
        return JsonResponse({'success': False, 'error': 'Не указан ID ответа'})

    try:
        answer = Answer.objects.select_related('question__test').get(pk=answer_id)
        if answer.question.test.author != request.user:
            return JsonResponse({'success': False, 'error': 'Нет прав'})
    except Answer.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Ответ не найден'})

    if text is not None:
        answer.text = text
    if flag is not None:
        answer.flag = flag.lower() in ['true', '1', 'on']

    answer.save(update_fields=['text', 'flag'])
    return JsonResponse({'success': True, 'message': 'Ответ обновлен'})


@require_POST
def add_answer(request):
    question_id = request.POST.get('question_id')
    text = request.POST.get('text', '').strip()
    flag = request.POST.get('flag', 'false')

    if not question_id:
        return JsonResponse({'success': False, 'error': 'Не указан вопрос'})

    try:
        question = Question.objects.get(pk=question_id)
        if question.test.author != request.user:
            return JsonResponse({'success': False, 'error': 'Нет прав'})
    except Question.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Вопрос не найден'})

    if not text:
        return JsonResponse({'success': False, 'error': 'Текст ответа пустой'})

    answer = Answer.objects.create(
        question=question,
        text=text,
        flag=flag.lower() in ['true', '1', 'on']
    )

    counter = question.answers.count()

    html = render_to_string('tests/answer_block.html', {
        'answer': answer,
        'counter': counter
    })

    return JsonResponse({'success': True, 'html': html})
