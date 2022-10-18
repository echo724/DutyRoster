import os

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import datetime

service_account_email = 'duty-roster@duty-roster-calendar.iam.gserviceaccount.com'

SCOPES = 'https://www.googleapis.com/auth/calendar'
scopes = [SCOPES]

def build_service():

    filepath = os.path.expanduser('~/.config/token.json')
    credentials = ServiceAccountCredentials.from_json_keyfile_name(filename=filepath,scopes=SCOPES)

    http = credentials.authorize(httplib2.Http())

    service = build('calendar', 'v3', http=http)

    return service

RANK_IN_KOREAN = {
    1:"이병",
    2:"일병",
    3:"상병",
    4:"병장"
}

def create_cq(rank,name,start_date):
    service = build_service()
    
    title = f"{RANK_IN_KOREAN[rank]} {name}"
    event = service.events().insert(calendarId='3qsv30e8454h9nfdoodatee98c@group.calendar.google.com', body={
        'summary': title,
        'start': {'date': start_date.isoformat()},
        'end': {'date':start_date.isoformat()}
    }).execute()

def create_other_duty(rank,name,start_date,duty_type):
    service = build_service()
    
    title = f"{duty_type} {RANK_IN_KOREAN[rank]} {name}"
    event = service.events().insert(calendarId='j6uo2gf0vc9abhglvigncbr5gk@group.calendar.google.com', body={
        'summary': title,
        'start': {'date': start_date.isoformat()},
        'end': {'date':start_date.isoformat()}
    }).execute()

def create_leaves(rank,name,start_date,end_date):
    service = build_service()
    end_date = end_date + datetime.timedelta(days=1)
    title = f"{RANK_IN_KOREAN[rank]} {name}"
    event = service.events().insert(calendarId='5p2l8tbjpqma2e3d0ualt7gsqg@group.calendar.google.com', body={
        'summary': title,
        'start': {'date': start_date.isoformat()},
        'end': {'date':end_date.isoformat()}
    }).execute()