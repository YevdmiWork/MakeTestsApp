from django.urls import reverse

menu = [
    {'title': "Создать тест", 'url_name': 'tests:add_test'},
    {'title': "Все тесты", 'url_name': 'tests:tests_all'},
]

def common_context(request):
    context = {'menu': menu}
    if request.user.is_authenticated:
        context['profile_url'] = reverse(
            'users:profile',
            kwargs={'username': request.user.username}
        )
    return context
