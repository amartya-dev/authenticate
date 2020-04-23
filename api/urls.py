from django.urls import path
from api.views import UserRegistrationView, TestApi


app_name = 'api'
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register_user'),
    path('home/', TestApi.as_view(), name='home')
]
