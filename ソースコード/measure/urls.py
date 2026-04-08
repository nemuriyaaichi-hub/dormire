from django.urls import path

from . import views

app_name = "measure"
urlpatterns = [
    path("", views.MeasureCreateView.as_view(), name="create"),
]
