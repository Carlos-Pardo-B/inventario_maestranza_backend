from django.urls import path
from .views import *
from django.http import HttpResponse

urlpatterns = [
    path('', index),
]