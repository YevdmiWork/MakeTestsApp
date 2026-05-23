class AppError(Exception):
    code = 'app_error'
    status_code = 400

    def __init__(self, message=None, details=None):
        self.message = message or self.code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self):
        return {
            'success': False,
            'error': {
                'code': self.code,
                'message': self.message,
                'details': self.details
            }
        }


class AppValidationError(AppError):
    code = 'validation_error'
    status_code = 400

    def __init__(self, errors: list[str]):
        super().__init__(
            message='Validation failed',
            details={
                'errors': errors
            }
        )


class PublishValidationError(AppError):
    code = 'publish_validation_error'
    status_code = 400

    def __init__(self, errors: list[str]):
        super().__init__(
            message='Publish validation failed',
            details={
                'errors': errors
            }
        )

class BadRequest(AppError):
    code = 'bad_request'
    status_code = 400


class NotFoundError(AppError):
    code = 'not_found'
    status_code = 404


class AccessDeniedError(AppError):
    code = 'access_denied'
    status_code = 403


class ConflictError(AppError):
    code = 'conflict_error'
    status_code = 409
