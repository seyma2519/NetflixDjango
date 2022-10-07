from tkinter import Y
from unicodedata import name
from django.urls import path
from .views import *

urlpatterns = [ 
    path('register/', userRegister, name='register'),
    path('login/', userLogin, name="login"),
    path('logout/', userLogout, name='logout' ),
    path('profile/', profile, name='profile'),
    path('create/', createProfile, name='create'),
    path('hesap/', hesap, name="hesap"),
    path('delete/', userDelete, name="delete"),
    path('update/',update, name='update')
]