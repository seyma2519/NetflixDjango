from django.urls import path
from .views import *

 
urlpatterns =  [ 
    path('', index, name='index'),
    path('movies/<str:slug>', movies, name='movies'),
    path('video/<int:id>', videolar, name='video')
]