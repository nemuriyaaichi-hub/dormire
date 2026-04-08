from django.urls import path

from . import views

app_name = "recommends"
urlpatterns = [
    path("", views.RecommendCreateView.as_view(), name="create"),
]
