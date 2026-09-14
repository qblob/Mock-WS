from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("app/admin/", admin.site.urls),
    path("app/", include("users.urls")),
]