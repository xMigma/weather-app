from distutils.log import error
from pydoc import resolve
import requests
import json
from django.shortcuts import render

BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?q='
API_KEY = '267d5a6861d7d54d0c3ed913fec66929'

def get_city_by_ip():
    ip = requests.get('https://api.ipify.org').text
    res = requests.get('http://ip-api.com/json/' + ip)
    return res.json()['city']

default_city = get_city_by_ip()    

def get_weather(request, city, error):
    url = BASE_URL + city + '&appid=' + API_KEY
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
        'error': error
    }
    return context


def index(request):
    global default_city
    if request.method == 'POST':
        city = request.POST.get('city')
    else:
        city = default_city

    try:
        url = BASE_URL + city + '&appid=' + API_KEY
        response = requests.get(url).json()
        default_city = response['name']
        return render(request, 'index.html', get_weather(request, city, None))
    except KeyError:
        return render(request, 'index.html', get_weather(request, default_city, 'Insert a valid city name'))
