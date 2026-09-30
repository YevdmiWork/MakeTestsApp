from unittest.mock import Mock

from ..constants.search import SEARCH_PARAM
from ..views.pages import AllTests


def test_invalid_sort(rf):
    request = rf.get('/tests/?sort_by=wrong')
    view = AllTests()
    view.request = request

    assert view.get_current_sort() == '-completion'


def test_apply_search(rf):
    request = rf.get(f'/tests/?{SEARCH_PARAM}=iq tests')
    view = AllTests()
    view.request = request

    qs = Mock()
    qs.search.return_value = qs

    view.apply_search(qs)

    qs.search.assert_called_once_with('iq tests')


def test_empty_search(rf):
    request = rf.get(f'/tests/?{SEARCH_PARAM}=')
    view = AllTests()
    view.request = request

    qs = Mock()

    view.apply_search(qs)

    qs.search.assert_not_called()
