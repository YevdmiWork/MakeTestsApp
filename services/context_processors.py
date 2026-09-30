from django.urls import reverse

from .menu import MENU


def common_context(request):
    menu = [
        {
            'title': item['title'],
            'url': reverse(item['url_name']),
        }
        for item in MENU
    ]

    context = {'menu': menu}

    if request.user.is_authenticated:
        context['profile_url'] = request.user.get_profile_url()

    return context
