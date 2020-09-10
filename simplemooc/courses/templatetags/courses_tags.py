from django import template

register = template.Library()

from courses.models import Enrollment


@register.simple_tag
def my_courses(user):
    return Enrollment.objects.filter(user=user)
