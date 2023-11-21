from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("get_offers", views.get_offers_selenium_req, name="get_offers"),
]