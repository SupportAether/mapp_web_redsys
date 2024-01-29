from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("payment/", views.make_payment, name="make_payment"),
    path("success/", views.make_payment, name="success"),
]