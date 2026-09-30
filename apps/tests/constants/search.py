SEARCH_PARAM = 'search'

SEARCH_THRESHOLD = 0.05

SEARCH_WEIGHTS = {
    'title': 0.5,
    'content': 0.2,
    'tag': 0.2,
    'author': 0.1,
}

SEARCH_ORDERING = (
    '-similarity',
    '-time_update',
)
