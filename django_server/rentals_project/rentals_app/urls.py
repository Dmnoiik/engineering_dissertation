from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("offers_page", views.offers_page, name="offers_page"),
    path("get_offers", views.get_offers_otodom, name="get_offers"),
    path("get_districts/<str:city>", views.get_districts, name="get_districts"),
]