from .models import Coefficient, Katusa
from django.db.models import Sum


def get_total_score(dates, rank):
    total_score = dates * Coefficient.objects.first().dates \
        + rank * Coefficient.objects.first().rank
    return total_score


def update_dates_score(katusa):
    this_dates_scores = list(katusa.this_duty_dates.aggregate(
        Sum('date_score')).values())[0] if katusa.this_duty_dates.all() else 0
    katusa.this_duty_dates_score = this_dates_scores
    total_score = get_total_score(this_dates_scores, katusa.rank)
    katusa.total_score = total_score
    katusa.save()


def update_all_katusa():
    for katusa in Katusa.objects.iterator():
        update_dates_score(katusa)
