from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied


class AdminRequiredMixin(AccessMixin):
    """Verify that the current user is in 'Admin' group."""

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.groups.filter(name="Admin").exists():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class InstructorRequiredMixin(AccessMixin):
    """Verify that the current user is in 'Instructor' group."""

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.groups.filter(name="Instructor").exists():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class StudentRequiredMixin(AccessMixin):
    """Verify that the current user is in 'Student' group."""

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.groups.filter(name="Student").exists():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class NameSearchMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.reqeust.GET.get("q")
        if query:
            queryset = queryset.filter(name__icontains=query)

        return queryset
