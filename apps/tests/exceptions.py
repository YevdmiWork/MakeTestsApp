class AppError(Exception):
    code = 'app_error'
    status_code = 400

    def __init__(self, message=None):
        self.message = message or self.code
        super().__init__(self.message)

    def to_dict(self):
        return {
            'error': self.code,
            'message': self.message
        }


class AppValidationError(AppError):
    code = 'validation_error'
    status_code = 400

    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__('Validation failed')

    def to_dict(self):
        return {
            'error': self.code,
            'errors': self.errors
        }


class PublishValidationError(AppError):
    code = 'publish_validation_error'
    status_code = 400

    def __init__(self, errors):
        self.errors = errors
        super().__init__('Publish validation failed')

    def to_dict(self):
        return {
            'error': self.code,
            'errors': self.errors
        }


class BadRequest(AppError):
    code = 'bad_request'
    status_code = 400


class NotFoundError(AppError):
    code = 'not_found'
    status_code = 404


class AccessDeniedError(AppError):
    code = 'access_denied'
    status_code = 403
