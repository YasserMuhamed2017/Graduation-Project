from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def get_date_range(start_date, end_date):
    """Returns list of dates between start_date and end_date."""
    if not start_date or not end_date:
        return []
    delta = end_date - start_date
    return [start_date + timedelta(days=i) for i in range(delta.days + 1)]
