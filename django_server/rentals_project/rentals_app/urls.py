from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("offers_page", views.offers_page, name="offers_page"),
    path("get_offers_otodom", views.get_offers_otodom, name="get_offers_otodom"),
    path("get_offers_olx", views.get_offers_olx, name="get_offers_olx"),
    path("get_districts/<str:city>", views.get_districts, name="get_districts"),
]