import requests
import json
from urllib import response
from django.shortcuts import render

BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?'
API_KEY = '267d5a6861d7d54d0c3ed913fec66929'

def index(request):
    ip = requests.get('https://api.ipify.org').text
    res = requests.get('http://ip-api.com/json/' + ip)

    if request.method == 'POST':
        city = request.POST.get('city')
    else:
        city = res.json()['city']

    url = BASE_URL + 'q=' + city + '&appid=' + API_KEY
    response = requests.get(url).json()

    context = {
        'city': response['name'],
        'country': response['sys']['country'],
        'temperature': round(response['main']['temp'] - 273.15),
        'min_temp': round(response['main']['temp_min'] - 273.15),
        'max_temp': round(response['main']['temp_max'] - 273.15),
        'description': response['weather'][0]['description'],
        'humidity': response['main']['humidity'],
        'pressure': response['main']['pressure'],
        'wind': round(response['wind']['speed'], 1),
        
    }    
    return render(request, 'city.html', context)
