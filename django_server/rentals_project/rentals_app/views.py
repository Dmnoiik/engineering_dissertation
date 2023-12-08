import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.core.cache import cache
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