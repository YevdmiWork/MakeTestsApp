from functools import wraps
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .constants.messages import UserMessages
from .exceptions import AppError, AuthenticationError
from .views.responses import success_response


def require_authentication(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise AuthenticationError(UserMessages.NOT_AUTH)

        return func(request, *args, **kwargs)

    return wrapper


def post_api(func):
    @wraps(func)
    @require_POST
    @handle_service_response
    @require_authentication
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def handle_service_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            data = func(*args, **kwargs)
            return JsonResponse(success_response(data), status=200)

        except AppError as e:
            return JsonResponse(e.to_dict(), status=e.status_code)

    return wrapper
