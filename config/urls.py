from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),

    # Django Login / Logout / Password Reset
    path("accounts/", include("django.contrib.auth.urls")),



    # College Admission App
    path("", include("admissions.urls")),
]


# Media files during local development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )