import django_filters

from .models import Class


class ClassFilter(django_filters.FilterSet):
    class Meta:
        model = Class
        fields = ["course", "semester", "is_active"]
