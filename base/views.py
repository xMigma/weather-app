from distutils.log import error
from operator import ge
from pydoc import resolve
import requests
import json
from django.shortcuts import render
from decouple import config

BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?q='
API_KEY = config('API_KEY')

def get_city_by_ip():
    ip = requests.get('https://api.ipify.org').text
    res = requests.get('http://ip-api.com/json/' + ip)
    return res.json()['city']

def index(request):
    global context
    if request.method == 'POST':
        city = request.POST.get('city')
    else:
        city = get_city_by_ip()

    try:
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
        }

    except KeyError:
        context['error'] = 'Insert a valid city name'

    return render(request, 'index.html', context)