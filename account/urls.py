from django.urls import path

from account.views import (
    account_search_view,
    account_view,
    edit_account_view,
    login_view,
    logout_view,
    register_view
)

app_name = 'account'

urlpatterns = [
    path('register/', register_view, name="register_view"),
    path('login/', login_view, name="login_view"),
    path('logout/', logout_view, name="logout_view"),
    path('profile/search/', account_search_view, name="account_search_view"),
    path('profile/<int:id>/', account_view, name="account_view"),
    path('profile/<int:id>/edit/', edit_account_view, name="edit_account_view"),
]
