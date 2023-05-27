import django_filters
from edu import models

class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = models.Task
        fields = ('section_id',)

class TestFilter(django_filters.FilterSet):
    class Meta:
        model = models.Test
        fields = ('title',)