from email import message
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Visitor, Test_project, High_level_tests
from django.http import HttpResponse
from .forms import ProjectForm, VisitorForm

def home(request):
    projects = Test_project.objects.all()
    context = {'projects': projects}

    return render(request, 'base/home.html', context)


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

def project(request, pk):
    project = Test_project.objects.get(id=pk)
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i
    context = {'project': project}
    return render(request, 'base/project_page.html', context)


def create_visitor(request):
    form = VisitorForm()
    if request.method == 'POST':
        form = VisitorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/visitor_form.html', context)

def update_visitor(request, pk):
    visitor = Visitor.objects.get(id=pk)
    form = VisitorForm(instance=visitor) # davame do formulare rovnou predvyplnena data odpovidajiciho uzivatele

    if request.method == 'POST':
        form = VisitorForm(request.POST, instance=visitor)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/visitor_form.html', context)


def create_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/testproject_form.html', context)

def update_project(request, pk): 
    project = Test_project.objects.get(id=pk)
    form = ProjectForm(instance=project) 

    if request.method== 'POST': 
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/testproject_form.html', context)


def delete_project(request, pk):
    project = Test_project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'object': project})

def list_visitors(request):
    visitors = Visitor.objects.all()
    context = {'visitors': visitors}
    #print(visitors.visible_test_projects.all())
    return render(request, 'base/see_visitors.html', context)

