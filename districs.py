import requests
import pandas as pd
import os
import os.path


class Gdansk:
    def __init__(self):
        self.file_present = os.path.isfile("dzielnice_gdanska.csv")
        self.districts = pd.read_csv("dzielnice_gdanska.csv", usecols=["Dzielnica"]).to_dict()["Dzielnica"] or None

    def create_district_files(self):
        get_table_with_districts("https://bip.gdansk.pl/urzad-miejski/Podzial-administracyjny-Gdanska,a,647", "dzielnice_gdanska.csv")
        self.file_present = os.path.isfile("dzielnice_gdanska.csv")
        self.districts = pd.read_csv("dzielnice_gdanska.csv", usecols=["Dzielnica"]).to_dict()["Dzielnica"]


    def display_districts(self):
        for id, district in self.districts.items():
            print(F"{id + 1}: {district}")

class Gdynia:
    def __init__(self):
        self.file_present = os.path.isfile("dzielnice_gdyni.csv")
        self.districts = None

    def create_district_files(self):
        get_table_with_districts("https://pl.wikipedia.org/wiki/Dzielnice_Gdyni", "dzielnice_gdyni.csv")
        self.file_present = os.path.isfile("dzielnice_gdyni.csv")
        self.districts = pd.read_csv("dzielnice_gdyni.csv", usecols=["Nazwa dzielnicy"]).to_dict()["Nazwa dzielnicy"]


    def display_districts(self):
        for id, district in self.districts.items():
            print(F"{id + 1}: {district}")

def get_table_with_districts(url_for_table, name_of_file):
    pd.read_html(requests.get(url_for_table).text)[0][:-1].to_csv(name_of_file)