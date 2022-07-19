from email import message
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import High_level_tests
from django.http import HttpResponse
from .forms import VisitorForm

def home(request):
    return render(request, 'base/home.html')


def logout_user(request):
    logout(request)
    return redirect('login')

def login_page(request):
    #if request.user.is_authenticated():
    #   return redirect('home')

    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Your account does not exist.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user) #pridame session do databaze, vytvorime cookies
            return redirect('home')
        else:
            message.error(request, 'Your account does not exist.')
    
    context = {}
    return render(request, 'base/login_autentizace.html', context)


def create_visitor(request):
    form = VisitorForm()
    if request.method == 'POST':
        print(request.post)
    context = {'form': form}
    return render(request, 'base/visitor_form.html', context)

