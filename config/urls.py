import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from diaries.views import DiaryDayListView

urlpatterns = [
    # Project urls
    path('', DiaryDayListView.as_view()),
    path('', include('profiles.urls')),
    path('food/', include('food.urls')),
    path('diary/', include('diaries.urls')),
    path('meals/', include('meals.urls')),
    path('progress/', include('progress.urls')),
    path('accounts/', include('accounts.urls')),
    path('blog/', include('blog.urls')),
    # Admin site
    path('admin/', admin.site.urls),
    # Admin password reset urls
    path(
        'admin/password_reset/',
        auth_views.PasswordResetView.as_view(),
        name='password_reset',
    ),
    path(
        'admin/password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path(
        'admin/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
    # Debug toolbar
    path('__debug__/', include(debug_toolbar.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
