from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from pet.models import Pet

def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('index')     
    else:
        return render(request, 'home.html')

def home(request):
    if request.user.is_authenticated:
        pets = Pet.objects.all()
        return render(request, 'index.html', {"pets": pets})
    else:
        return redirect('index')
