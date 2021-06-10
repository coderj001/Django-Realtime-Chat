from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('account/', include('account.urls', namespace='account')),


    # TODO:  <10-06-21, coderj001> # Password reset through templates not done
    path('password_change/done', auth_views.PasswordChangeDoneView.as_view(),
         name="password_change_done"),
    path('password_change/', auth_views.PasswordChangeView.as_view(),
         name="password_change"),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name="password_reset"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
