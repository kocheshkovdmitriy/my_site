import django_filters
from django.db.models import Q

from users import models


class ProfileFilter(django_filters.FilterSet):
    user__first_name__icontains = django_filters.CharFilter(label='Имя')
    school__icontains = django_filters.CharFilter(label='Школа')
    grade = django_filters.NumberFilter(label='Класс')

    class Meta:
        model = models.Profile
        fields = []

    def filter_queryset(self, queryset):
        data = dict()
        for name, value in self.form.cleaned_data.items():
            if value:
                data[name] = value
        queryset = queryset.filter(Q(_connector="OR", **data))
        return queryset
