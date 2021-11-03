import requests

class TrainManager():

    def __init__(self):
        self.raw_data = dict()
        self.raw_included = dict()
        pass

    def get(self, url):
        raw = requests.get(url).json()
        self.raw_data = raw['data']
        self.raw_included = raw['included']



    def cast_time(self, time):
        if time is not None:
            return time[11:19]
        return "Soon"