from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path, re_path

admin.site.site_header = "Dormire 管理画面"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("auth.urls")),
    path("recommends/", include("recommends.urls")),
    path("measure/", include("measure.urls")),
    path("orders/", include("orders.urls")),
    re_path(r"^health$", lambda r: HttpResponse()),
]
