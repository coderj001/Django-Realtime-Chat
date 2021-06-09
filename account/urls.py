from django.urls import path

from account.views import register_view, login_view, logout_view

app_name = 'account'

urlpatterns = [
    path('register/', register_view, name="register_view"),
    path('login/', login_view, name="login_view"),
    path('logout/', logout_view, name="logout_view"),
]
