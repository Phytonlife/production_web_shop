from django.urls import path
from .views import WebUserRegistrationView

urlpatterns = [
    path('register/', WebUserRegistrationView.as_view(), name='register'),
]
