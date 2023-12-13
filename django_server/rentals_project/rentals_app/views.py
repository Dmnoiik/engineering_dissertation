import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.cache import cache
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
import json
from .models import FavoriteOffer
# Create your views here.

def index(request):
    return render(request, "index.html")


def offers_page(request):
    return render(request, "offers_page.html")


def get_offers_otodom(request):
    from .scripts import otodom_selenium
    try:
        district_result = request.GET.get("district")
        town_result = request.GET.get("town")
        cache_key_otodom = f"otodom_offers_{town_result}_{district_result}"
        cached_offers = cache.get(cache_key_otodom)
        if cached_offers is None:
            result_otodom = otodom_selenium.get_offers_otodom(district_result, town_result)
            cache.set(cache_key_otodom, result_otodom, timeout=3600)
            return JsonResponse({"offers": result_otodom})
        else:
            return JsonResponse({"offers": cached_offers})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_offers_olx(request):
    from .scripts import olx_selenium
    try:
        district_result = request.GET.get("district")
        town_result = request.GET.get("town")
        cache_key_olx = f"olx_offers_{town_result}_{district_result}"
        cached_offers = cache.get(cache_key_olx)
        if cached_offers is None:
            result_olx = olx_selenium.get_offers_olx(district_result, town_result)
            cache.set(cache_key_olx, result_olx, timeout=3600)
            return JsonResponse({"offers": result_olx})
        else:
            return JsonResponse({"offers": cached_offers})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_districts(request, city):
    if city == "Gdańsk":
        districts = pd.read_csv("rentals_app/scripts/dzielnice_gdanska.csv", usecols=["Dzielnica"]).to_dict()[
            "Dzielnica"]
        return JsonResponse({"districts": districts})
    elif city == "Gdynia":
        districts = pd.read_csv("rentals_app/scripts/dzielnice_gdyni.csv", usecols=["Nazwa dzielnicy"]).to_dict()[
            "Nazwa dzielnicy"]
        return JsonResponse({"districts": districts})


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.login(request)
            if user:
                return redirect('dashboard')
    else:
        form = UserLoginForm()
    return render(request, "registration/login.html", {"form": form})


def registration_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Create a new user account
            if user:
                login(request, user)
                return redirect('dashboard')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/registration.html', {'form': form})


@login_required
def dashboard_view(request):
    user = request.user
    favorite_offers = FavoriteOffer.objects.filter(user=user).all()
    return render(request, "dashboard.html", {"user": user, "favorite_offers": favorite_offers})

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
@require_POST
@csrf_protect
def toggle_favorite_offer(request):
    data = json.loads(request.body)
    user = request.user
    offer_id = data["offer_id"]

    favorite_offer = FavoriteOffer.objects.filter(user=user, offer_id=offer_id).first()
    if favorite_offer:
        favorite_offer.delete()
        return JsonResponse({"status": "removed", "offer_id": offer_id})
    else:
        FavoriteOffer.objects.create(
            user=user,
            offer_id=offer_id,
            link=data["link"],
            image_link=data["image_link"],
            price=data["price"],
            rent=data["rent"],
            address=data["address"],
            rooms=data["rooms"],
            surface=data["surface"],
            website=data["website"]
        )
        return JsonResponse({"status": "added", "offer_id": offer_id})
    return JsonResponse({"status": "error"}, status=404)