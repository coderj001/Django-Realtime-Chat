from django.urls import path

from account.views import login_view, logout_view, register_view

app_name = 'account'

urlpatterns = [
    path('register/', register_view, name="register_view"),
    path('login/', login_view, name="login_view"),
    path('logout/', logout_view, name="logout_view"),


]
