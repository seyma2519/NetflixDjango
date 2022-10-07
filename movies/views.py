
from multiprocessing import context
from re import search
from django.shortcuts import render
from .models import *
from user.models import Profile
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'index.html')

def movies(request, slug):
    profil = Profile.objects.get(slug = slug)
    profiles = Profile.objects.filter(user =request.user)
    filmler = Movie.objects.all()



    search = ''
    if request.GET.get('search'):  #search get olarak geldiyse
        search = request.GET.get('search')
        filmler = Movie.objects.filter(
            Q(isim__icontains = search) |
            Q(kategori__isim__icontains = search)
        ) 


    context = {
        'filmler':filmler,
        'profil':profil,
        'profiles':profiles,
        'search':search
    }
    return render(request, 'browse-index.html', context)

def videolar(request, id):
    video = Movie.objects.get(id = id)
    context = {
        'video':video
    }
    return render(request, 'video.html', context)