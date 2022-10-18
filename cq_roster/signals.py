from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ThisDutyDate, Coefficient
from .helpers import update_dates_score, update_all_katusa
from django.db.models import Sum


@receiver(post_save, sender=ThisDutyDate)
def worker_post_save(sender, **kwargs):
    katusa = kwargs["instance"].worker
    update_dates_score(katusa)


@receiver(post_save, sender=Coefficient)
def coefficient_post_save(sender, **kwargs):
    update_all_katusa()
