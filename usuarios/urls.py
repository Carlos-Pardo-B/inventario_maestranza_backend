from django.urls import path
from .views import LoginView, RegistroView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registro/', RegistroView.as_view(), name='registro'),
]
