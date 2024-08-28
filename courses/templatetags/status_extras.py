from django import template

from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def status_icon(condition):
    if condition:
        return format_html(
            mark_safe('<i class="bi bi-check-circle-fill text-success"></i>')
        )
    else:
        return format_html(mark_safe('<i class="bi bi-x-circle-fill text-danger"></i>'))


@register.filter
def status_badge(value):
    """Return badge class based on the status of 'Active' and 'Inactive'."""
    if value == "ACTIVE":
        return "badge text-bg-success"
    elif value == "INACTIVE":
        return "badge text-bg-danger"
    return "badge"


@register.filter
def semester_status_badge(value):
    """Return badge class based on the semester status."""
    if value == "ACT":
        return "badge text-bg-primary"
    elif value == "COMP":
        return "badge text-bg-success"
    elif value == "ARC":
        return "badge text-bg-danger"
    return "badge"


@register.filter
def enrollment_status_badge(value):
    """Return badge class based on the enrollment status."""
    if value == "ACTIVE":
        return "badge text-bg-success"
    elif value == "DROPPED":
        return "badge text-bg-danger"
    return "badge"


@register.filter
def attendance_status_badge(value):
    """Return badge class based on the attendance status."""
    if value == "PRE":
        return "badge text-bg-success"
    elif value == "ABS":
        return "badge text-bg-danger"
    return "badge"
