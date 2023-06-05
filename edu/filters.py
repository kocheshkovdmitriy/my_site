import django_filters
from edu import models

class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = models.Task
        fields = ('section_id',)

class TestFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(label="Тема теста", lookup_expr='icontains')

    class Meta:
        model = models.Test
        fields = ('title',)