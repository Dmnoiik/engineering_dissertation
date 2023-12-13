from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path("", views.index, name="index"),
    path("offers_page", views.offers_page, name="offers_page"),
    path("get_offers_otodom", views.get_offers_otodom, name="get_offers_otodom"),
    path("get_offers_olx", views.get_offers_olx, name="get_offers_olx"),
    path("get_districts/<str:city>", views.get_districts, name="get_districts"),
    path("login_user", views.login_view, name="login"),
    path('register_user', views.registration_view, name="registration"),
    path("dashboard", views.dashboard_view, name="dashboard"),
    path("logout_user", LogoutView.as_view(), name="logout"),
    path("toggle_favorite", views.toggle_favorite_offer, name="toggle_favorite_offer")
]