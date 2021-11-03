from django.urls import include, path
from api import views

urlpatterns = [
        path('', views.index, name='index'),
        path('home', views.home, name='home'),
        path('about', views.about, name='about'),
        path('cars', views.cars, name='cars'),
]
