from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def userRegister(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        resim = request.FILES['resim']
        tel = request.POST['tel']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username = username).exists():
                messages.error(request, 'Kullanıcı adı kullanımda')
                return redirect('register')
            elif User.objects.filter(email = email).exists():
                messages.error(request, 'Email kullanımda')
                return redirect('register')
            elif username in password1:
                messages.error(request, 'Kullanıcı adı ile şifre benzer olamaz')
                return redirect('register')
            elif len(password1) < 6:
                messages.error(request, 'Şifre en az 6  karakter olmalı')
                return redirect('register')
            else:
                user = User.objects.create_user(username = username, email = email, password = password1)
                Account.objects.create(
                    user = user,
                    resim = resim,
                    tel = tel

                )
                subject = 'Neos Netflix'
                message = 'Bu Netflix projesini 25 Temmuz grubuyla beraber yaptık.'
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False

                )
                user.save()
                messages.success(request, 'Kullanıcı oluşturuldu')
                return redirect('index')
    return render(request, 'user/register.html')

def userLogin(request):
    if request.method  == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Giriş yapıldı')
            return redirect('profile')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı')
            return redirect('login')
    return render(request, 'user/login.html')

def userLogout(request):
    logout(request)
    messages.success(request, 'Çıkış yapıldı')
    return redirect('index')

def profile(request):
    profiles = Profile.objects.filter(user = request.user)
    context = {

       'profiles': profiles
    }
    return render(request, 'browse.html', context)

def createProfile(request):
    form = ProfileForm()
    profile = Profile.objects.filter(user = request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if len(profile) < 4 :
            if form.is_valid():
               profil = form.save(commit = False)
               profil.user = request.user
               profil.save()
               messages.success(request, 'profil olusturuldu')
               return redirect('profile')
        else:
            messages.error(request, 'Profil sayısı 4 ten fazlaa olamaz')
            return redirect('request')
    context = {
        'form':form
    }
    return render(request, 'createProfile.html', context)

def hesap(request):
    user = request.user.account
    context = {
        'user':user
    }
    return render(request, 'user/hesap.html', context)

def userDelete(request):
    user = request.user
    user.delete()
    messages.success(request, 'Kullanıcı Silindi')
    return redirect("index")

def update(request):
    user =request.user.account
    form = AccountForm(instance = user)
    if request.method =='POST':
        form = AccountForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profiliniz guncellendi')
            return redirect("hesap")
    context = {
        'form':form
    }
    return render(request, 'user/update.html', context)