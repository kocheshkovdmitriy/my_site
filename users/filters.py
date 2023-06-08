import django_filters
from django.db.models import Q

from users import models


class ProfileFilter(django_filters.FilterSet):
    user__first_name__icontains = django_filters.CharFilter(label='Имя')
    user__last_name__icontains = django_filters.CharFilter(label='Фамилия')
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
        queryset = queryset.filter(Q(user__is_staff=False) & Q(_connector="OR", **data))
        return queryset
