import pytest

from ..constants.limits import TestLimits
from ..exceptions import AppValidationError
from ..validators.test import validate_test_title, validate_test_content


class TestValidateTitle:
    def test_less_than_min(self):
        title = 'a' * (TestLimits.TITLE_MIN_LENGTH - 1)

        with pytest.raises(AppValidationError):
            validate_test_title(title=title)

    def test_equal_min(self):
        title = 'a' * TestLimits.TITLE_MIN_LENGTH

        validate_test_title(title=title)

    def test_equal_max(self):
        title = 'a' * TestLimits.TITLE_MAX_LENGTH

        validate_test_title(title=title)

    def test_greater_than_max(self):
        title = 'a' * (TestLimits.TITLE_MAX_LENGTH + 1)

        with pytest.raises(AppValidationError):
            validate_test_title(title=title)


class TestValidateContent:
    def test_equal_max(self):
        content = 'a' * TestLimits.CONTENT_MAX_LENGTH

        validate_test_content(content=content)

    def test_greater_than_max(self):
        content = 'a' * (TestLimits.CONTENT_MAX_LENGTH + 1)

        with pytest.raises(AppValidationError):
            validate_test_content(content=content)
