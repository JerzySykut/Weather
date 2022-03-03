import json
import time
from datetime import date, datetime
from os.path import exists
import requests

class WeatherForecast(object):
    def __init__(self, apiKey: str):
        self.apiKey = apiKey
        self.storedData = dict()
        self.n = 0
        self.loadFromFile()

    def loadFromFile(self):
        if exists('storedData.json'):
            with open('storedData.json', 'r') as f:
                self.storedData = json.load(f)
    def saveToFile(self):
        with open('storedData.json', 'w') as f:
            json.dump(self.storedData, f)
    def loadFromApi(self):
        url = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"
        querystring = {"q":"Wroclaw,pl","lang":"pl","units":"metric","cnt":"16","mode":"json"}
        headers = {
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
            'x-rapidapi-key': self.apiKey
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        wData = response.json()
        for item in wData['list']:
            wItem = self.itemFromJsonItem(item)
            self.storedData.update({ wItem['dt'] : wItem })
        self.saveToFile()
    def itemFromJsonItem(self, jsonItem):
        d = date.fromtimestamp(int(jsonItem['dt']))
        return {
            'dt' : d.strftime('%Y-%m-%d'),
            'weather_main' : jsonItem['weather'][0]['main'],
            'weather_description' : jsonItem['weather'][0]['description']
        }
    def __iter__(self):
        self.n = 0
        return self
    def __next__(self):
        if len(self.storedData) == 0 or len(self.storedData) <= self.n - 1:
            return StopIteration
        key = self.storedData.keys()[self.n]
        result = self.storedData[key]
        self.n += 1
        return result
    def __getitem__(self, key: str):
        if key not in self.storedData:
            self.loadFromApi()  #nie mamy info z pliku, próbujemy doczytać z api
        if key not in self.storedData:
            return {'dt' : key, 'weather_main' : 'Unknown', 'weather_description' : 'nie wiem'}
        else:
            return self.storedData[key]

    def items(self):
        return ((i['dt'], i['weather_description']) for i in self.storedData.values())
