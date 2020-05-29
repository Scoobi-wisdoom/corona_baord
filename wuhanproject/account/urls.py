from django.contrib import admin
from django.urls import path
from .views import (
    registration_view,
    login_view,
    logout_view,
    account_view,
    must_authenticate_view,
)

app_name = 'account'

urlpatterns = [
    path('', account_view, name='account'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('must_authenticate/', must_authenticate_view, name='must_authenticate'),
    path('register/', registration_view, name='register'),
]
