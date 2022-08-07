import requests
import json
from urllib import response
from django.shortcuts import render

BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?'
API_KEY = '267d5a6861d7d54d0c3ed913fec66929'

def index(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        url = BASE_URL + 'q=' + city + '&appid=' + API_KEY
        response = requests.get(url).json()
        context = {
            'city': response['name'],
            'country': response['sys']['country'],
            'temperature': round(response['main']['temp'] - 273.15),
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon']
        }
        return render(request, 'city.html', context)
    return render(request, 'city.html')    