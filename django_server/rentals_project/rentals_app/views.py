import json

from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index(request):
    return render(request, "base.html")


def get_offers_selenium_req(request):
    from .scripts import test
    try:
        result = test.get_offers()
        return JsonResponse({"offers": result})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
