from functools import wraps
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .exceptions import AppError
from .views.responses import success_response


def post_api(func):
    @wraps(func)
    @require_POST
    @handle_service_response
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
