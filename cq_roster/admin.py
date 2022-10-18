from django.contrib import admin
from django.db.models import query
from .models import (
    Katusa,
    ThisDutyDate,
    NextDutyDate,
    Coefficient,
    OtherDutyDate,
    Leave
)
from .actions import *
# Register your models here.

@admin.register(Katusa)
class KatusaAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "rank",
        "section_name",
        'is_rso',
        "this_month_duties",
        "next_month_duties",
        "total_score",
    )

    def section_name(self, obj):
        return obj.section

    def this_month_duties(self, obj):
        return list(obj.this_duty_dates.all())

    def next_month_duties(self, obj):
        return list(obj.next_duty_dates.all())

    ordering = ["-total_score"]
    readonly_fields = ["this_duty_dates_score", "total_score"]
    actions = [update_score]

@admin.register(OtherDutyDate)
class OtherDutyDateAdmin(admin.ModelAdmin):
    list_display = ("duty_date", "duty_type", "worker", 'date_type')
    ordering = ['duty_date','duty_type']
    actions = [save_items,create_other_duty_calendar_events,swap_workers]

@admin.register(ThisDutyDate)
class ThisDutyDateAdmin(admin.ModelAdmin):
    list_display = ("duty_date", "date_score", "worker")
    actions = [save_items,create_cq_calendar_events,swap_workers]


@admin.register(NextDutyDate)
class NextDutyDateAdmin(admin.ModelAdmin):
    list_display = ("duty_date", "date_score", "worker")
    actions = [assign_workers,clear_next_month,create_cq_calendar_events,swap_workers]

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('personnel','start_date','end_date')
    actions = [create_leave_calendar_events]
    ordering = ['start_date']

admin.site.register([Coefficient])