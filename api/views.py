import requests
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Car
from .serializers import CarSerializer

# Create your views here.

def index(request):
    link = 'https://api-v3.mbta.com/predictions?page%5Boffset%5D=0&page%5Blimit%5D=10&sort=departure_time&include=schedule%2Ctrip&filter%5Bdirection_id%5D=0&filter%5Bstop%5D=place-north'

    response = requests.get(link).json()
    included = response['included']
    
    for prediction in response['data']:
        schedule_id = prediction['relationships']['schedule']['data']['id']
        for record in included:
            if record['id'] == schedule_id:
                prediction['schedule_time'] = record['attributes']['departure_time']

    return JsonResponse(response['data'], safe=False)

def about(request):
    return HttpResponse("About") 

def home(request):
    return HttpResponse("Home")

def cars(request):
    return HttpResponse("Cars")
