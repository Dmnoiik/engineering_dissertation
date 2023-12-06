import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render

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
        result = otodom_selenium.get_offers(district_result, town_result)
        return JsonResponse({"offers": result, "website": "otodom"})
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