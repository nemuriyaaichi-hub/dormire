from dj_rest_auth.views import LoginView
from django.urls import path

app_name = 'auth'
urlpatterns = [
    path('signin/', LoginView.as_view(), name='signin'),
]
