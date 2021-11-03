import requests
from django.db import models
import pytz


# Create your models here.
from ElsysPrimerno.trainManager import TrainManager


class Car(models.Model):
    color = models.CharField(max_length=100)
    made = models.DateTimeField(auto_now_add=True)
    brand = models.CharField(max_length=100)
    description = models.TextField()


# Vazhno e da se pravqt migracii! Zashtoto inache stava andibul morkov.

class Prediction(models.Model):
    time = models.TimeField
    destination = models.CharField(max_length=100)
    train = models.CharField(max_length=50)
    status = models.CharField(max_length=20)

    tz_NY = pytz.timezone('America/New_York')

    def __init__(self, time_input, destination_input, train_input, status_input):
        self.time = time_input
        self.destination = destination_input
        self.train = train_input
        self.status = status_input

    trainManager = TrainManager()

    @staticmethod
    def extract_destination(entry):
        trip_id = entry['relationships']['trip']['data']['id']

        get_trip = requests.get('https://api-v3.mbta.com/trips/' + trip_id)
        destination = get_trip.json()['data']['attributes']['headsign']

        return destination

    @staticmethod
    def extract_vehicle(entry):
        vehicle_id = entry['relationships']['vehicle']['data']['id']

        get_vehicle = requests.get('https://api-v3.mbta.com/vehicles/' + vehicle_id)
        vehicle = get_vehicle.json()['data']['attributes']['label']

        return vehicle

    def __str__(self):
        self.time = self.trainManager.cast_time(self.time)
        return self.time + '---' + self.destination + '---' + self.train
