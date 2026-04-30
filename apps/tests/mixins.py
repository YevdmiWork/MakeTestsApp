from django.http import Http404

from .models.choices import TestStatus


class PublishedTestMixin:

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.status != TestStatus.PUBLISHED.value:
            raise Http404()
        return obj
