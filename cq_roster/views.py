from django.shortcuts import render
from .models import Katusa,ThisDutyDate,NextDutyDate
import json

# Create your views here.
def index(request):
    katusas = list(Katusa.objects.all().order_by("-rank"))
    this_duty_dates = ThisDutyDate.objects.all()
    this_duty_dates_js = [this_duty_date.to_json() for this_duty_date in this_duty_dates]

    next_duty_dates = NextDutyDate.objects.all()
    next_duty_dates_js = [next_duty_date.to_json() for next_duty_date in next_duty_dates]
    context = {
        'katusas' : katusas,
        'this_duty_dates_js': json.dumps(this_duty_dates_js,ensure_ascii = False),
        'next_duty_dates_js': json.dumps(next_duty_dates_js,ensure_ascii = False)
    }
    return render(request,'cq_roster/index.html',context)

RANK = {
    1:"PV2",
    2:"PFC",
    3:"CPL",
    4:"SGT"
}
RANK_IN_KOREAN = {
    1:"이병",
    2:"일병",
    3:"상병",
    4:"병장"
}
OTHER_DUTY_KOREAN = {
    'KP':'KP',
    'GG':'짐가드'
}