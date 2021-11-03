import requests
from django.http import HttpResponse, JsonResponse
from .serializers import CarSerializer
from datetime import datetime

# Create your views here.
from django.shortcuts import render

from ElsysPrimerno.models import Car, Prediction
from .trainManager import TrainManager


def index(request):
    return HttpResponse("Hello, Django!")


def home(request):
    return render(request, 'home.html')


def list_cars(request):
    all_cars = Car.objects.all()
    return render(request, 'cars_list.html', {'cars': all_cars})


def cars_json(request):
    cars = Car.objects.all()
    return JsonResponse(CarSerializer(cars, many=True).data, safe=False)


def transport_endpoint(request):
    train_manager = TrainManager()

    # get_time = requests.get('https://api-v3.mbta.com/predictions?page%5Boffset%5D=0&page%5Blimit%5D=10&sort=departure_time&include=schedule%2Ctrip&filter%5Bdirection_id%5D=0&filter%5Bstop%5D=place-north')

    # Fetches the last 10 entries in the predictions table.
    train_manager.get('https://api-v3.mbta.com/predictions?page%5Boffset%5D=0&page%5Blimit%5D=10&sort=departure_time&include=schedule%2Ctrip&filter%5Bdirection_id%5D=0&filter%5Bstop%5D=place-north')

    predictions = []
    current_id = 0

    for prediction in train_manager.raw_data:
        data_dictionary = dict(prediction['attributes'])

        predictions.append(Prediction(None, None, None, data_dictionary['status']))

        print(current_id, ' -> ', prediction)

        current_id += 1

    print(train_manager.raw_included)

    return render(request, 'departure_board.html',
                  {'predictions': predictions, 'current_time': datetime.now(Prediction.tz_NY)})
