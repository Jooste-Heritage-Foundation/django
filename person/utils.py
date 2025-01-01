# person/utils.py

from datetime import date
from django.db.models import Q
from .models import Profile

def get_birthdays_in_next_three_months():
    today = date.today()
    current_month = today.month
    next_three_months = [(current_month + i - 1) % 12 + 1 for i in range(0, 3)]  # Next 3 months

    # Base query: alive people with birthdays in the next three months
    query = Q(vitality='A') & Q(birth_month__in=next_three_months)

    # Exclude past days in the current month
    if today.day > 1:
        query &= ~Q(birth_month=current_month, birth_day__lt=today.day)

    # Execute the query
    results = Profile.objects.filter(query)

    return results