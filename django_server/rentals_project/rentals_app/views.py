import json

import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, "index.html")


def get_offers_selenium_req(request):
    from .scripts import test
    try:
        district_result = request.GET.get("district")
        town_result = request.GET.get("town")
        print(town_result)
        result = test.get_offers(district_result, town_result)
        return JsonResponse({"offers": result})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def get_districts(request, city):
    print(city)
    if city == "gdansk":
        districts = pd.read_csv("rentals_app/scripts/dzielnice_gdanska.csv", usecols=["Dzielnica"]).to_dict()[
            "Dzielnica"]
        return JsonResponse({"districts": districts})
    elif city == "gdynia":
        districts = pd.read_csv("rentals_app/scripts/dzielnice_gdyni.csv", usecols=["Nazwa dzielnicy"]).to_dict()[
            "Nazwa dzielnicy"]
        return JsonResponse({"districts": districts})