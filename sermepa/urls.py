from django.urls import include, re_path, path
from . import views

urlpatterns = [
    path('ipn', view=views.sermepa_ipn, name='sermepa_ipn'),
]