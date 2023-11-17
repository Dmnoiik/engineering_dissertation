import pandas
from django.shortcuts import render
from django.http import HttpResponse
# from main import main_fun
# Create your views here.

def index(request):
    # info = main_fun()
    district = pandas.read_csv("C:/Users/dmars/Documents/PRACA_INZYNIERSKA/project_python/Śródmieście.csv")
    for x in district["Title"].values:
        print(x)
    return render(request, "base.html", {"offers": district["Title"].values})
