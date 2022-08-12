import requests
from django.shortcuts import render
from decouple import config

BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?q='
API_KEY = config('API_KEY')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_city_by_ip(request):
    try:
        ip = get_client_ip(request)
        res = requests.get('http://ip-api.com/json/' + ip)
        return res.json()['city']
    except KeyError:
        return 'London'

def index(request):
    global context
    if request.method == 'POST':
        city = request.POST.get('city')
    else:
        city = get_city_by_ip(request)
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