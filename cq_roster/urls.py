from django.urls import path

from . import views



app_name = "cq_roster"
urlpatterns = [
    path('',views.index,name="index"),
]