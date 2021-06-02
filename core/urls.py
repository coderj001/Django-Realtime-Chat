from core.views import home_view
from django.urls import path

app_name = 'core'

urlpatterns = [
    path('', home_view, name="home_view"),
]
