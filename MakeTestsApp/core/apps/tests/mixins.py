from django.db.models import Q
from django.http import HttpRequest


class SortingMixin:
    request: HttpRequest
    sort_dict = {
        'newest': '-time_update',
        'oldest': 'time_update',
        'popular': '-completion',
    }

    def sort_queryset(self, queryset):
        sort_by = self.request.GET.get('sort_by', 'popular')
        return queryset.order_by(self.sort_dict.get(sort_by, '-completion'))


class SearchMixin:
    request: HttpRequest
    search_options = [
        'title',
        'author__username',
        'tag__name',
        ]

    def filter_queryset(self, queryset):
        query = (self.request.GET.get('q') or '').strip()
        if not query:
            return queryset

        q_objects = Q()
        for option in self.search_options:
            q_objects |= Q(**{f"{option}__contains": query})

        return queryset.filter(q_objects).distinct()
