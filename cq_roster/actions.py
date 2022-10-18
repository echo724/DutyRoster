from django.contrib import admin
from .models import Katusa, ThisDutyDate
from .helpers import update_dates_score, update_all_katusa
from .google_calendar import create_cq,create_other_duty,create_leaves

@admin.action(description="Save selected items to update")
def save_items(modeladmin, request, queryset):
    for query in queryset.iterator():
        query.save()

@admin.action(description="Swap selected dates workers (select only two)")
def swap_workers(modeladmin, request, queryset):
    dates = list(queryset.all())
    katusa_id = dates[0].worker_id
    dates[0].worker_id = dates[1].worker_id
    dates[1].worker_id = katusa_id

    dates[0].save()
    dates[1].save()

@admin.action(description="Create CQ event in google calendar from selected dates")
def create_cq_calendar_events(modeladmin, request, queryset):
    dates = list(queryset.all())
    katusa = None
    for date in dates:
        katusa = Katusa.objects.get(id=date.worker_id)
        create_cq(katusa.rank,katusa.name,date.duty_date)

@admin.action(description="Create Other Duty event in google calendar from selected dates")
def create_other_duty_calendar_events(modeladmin, request, queryset):
    dates = list(queryset.all())
    katusa = None
    for date in dates:
        katusa = Katusa.objects.get(id=date.worker_id)
        create_other_duty(katusa.rank,katusa.name,date.duty_date,date.duty_type)

@admin.action(description="Create Leave event in google calendar from selected leaves")
def create_leave_calendar_events(modeladmin, request, queryset):
    leaves = list(queryset.all())
    katusa = None
    for leave in leaves:
        katusa = Katusa.objects.get(id=leave.personnel_id)
        create_leaves(katusa.rank,katusa.name,leave.start_date,leave.end_date)

@admin.action(description="Update selected katusas' score")
def update_score(self, request, queryset):
    for katusa in list(queryset.all()):
        update_dates_score(katusa)

@admin.action(description="Assign workers to duty dates")
def assign_workers(self, request, queryset):
    duty_dates = list(queryset.order_by("-date_score"))
    num_dates = len(duty_dates)
    katusas = list(
        Katusa.objects.exclude(section="RSO_HAS_DUTY").order_by("is_rso","total_score","rank")
    )
    num_katusas = len(katusas)
    num_rso_katusa = 5

    if num_dates > (num_katusas - num_rso_katusa):
        assign_katusa(num_dates, duty_dates, katusas)
    else:
        us_katusa = list(
            Katusa.objects.exclude(section="SENIOR")
            .exclude(section="RSO")
            .order_by("total_score")
        )
        assign_katusa(num_dates,duty_dates,us_katusa)

@admin.action(description="Move next month dates to this month dates")
def clear_next_month(self, request, queryset):
    duty_dates = list(queryset)
    ThisDutyDate.objects.all().delete()
    for next_date in duty_dates:
        ThisDutyDate.objects.create(
            duty_date=next_date.duty_date,
            date_score=next_date.date_score,
            worker_id=next_date.worker_id,
        )

    queryset.delete()

    update_all_katusa()

def assign_katusa(num_dates, duty_dates, katusas):
    num_katusas = len(katusas)
    for i in range(num_dates):
        i %= num_katusas
        duty_dates[i].worker_id = katusas[i].id
        duty_dates[i].save()