from django.urls import path

from account.views import register_view

app_name = 'account'

urlpatterns = [
    path('register/', register_view, name="register_view"),
]
