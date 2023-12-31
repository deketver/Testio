from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Visitor, Test_project, High_level_tests
from .forms import ProjectForm, VisitorForm, VisitorFormUser, VisitorFormUpdate, UploadFileForm
from django.db.models import Q
from django.db.models import Sum, Max
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from . data_load import load_file

@login_required(login_url='login')
def home(request):
    projects = Test_project.objects.all()
    
    if request.user.is_superuser == False:
        visitor = Visitor.objects.get(id=request.user.id)
        field_object = Visitor._meta.get_field('visible_test_projects')
        available_projects = field_object.value_from_object(visitor)
        print(available_projects)
        context = {'projects': available_projects}
        return render(request, 'base/home.html', context)
    else:
        context = {'projects': projects}
        return render(request, 'base/home.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


def login_page(request):
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
            messages.error(request, 'Your account does not exist.')
    
    context = {}
    return render(request, 'base/login_autentizace.html', context)

@login_required(login_url='login')
def project(request, pk):
    filter_active = False
    permission = request.user.is_superuser

    product = request.GET.get('product') if request.GET.get('product') != None else ''
    sfcode = request.GET.get('sfcode') if request.GET.get('sfcode') != None else ''
    family = request.GET.get('family') if request.GET.get('family') != None else ''
    status = request.GET.get('status') if request.GET.get('status') != None else ''
    failgroup = request.GET.get('failgroup') if request.GET.get('failgroup') != None else ''

    project = Test_project.objects.get(id=pk)
    available_data = High_level_tests.objects.filter(project=pk)

    distinct_names = High_level_tests.objects.all().values('name').distinct()
    distinct_sf_codes = High_level_tests.objects.all().values('sf_code').distinct()
    distinct_family = High_level_tests.objects.all().values('family').distinct()
    distinct_results = High_level_tests.objects.all().values('result').distinct()
    distinct_fail = High_level_tests.objects.all().values('fail_group_name').distinct()
    last_name = ''
    last_sf_code = ''
    last_family = ''
    last_result = ''
    last_fail = ''


    if product != '' or sfcode != '' or family != '' or status != '' or failgroup != '':
        available_data = High_level_tests.objects.filter(Q(name__icontains=product)
        & Q(sf_code__icontains=sfcode) & Q(family__icontains=family) & Q(result__icontains=status)
        & Q(fail_group_name__icontains=failgroup))
        last_name=product
        last_sf_code = sfcode
        last_family = family
        last_result = status
        last_fail = failgroup
        filter_active = True

    test_total = available_data.aggregate(Sum('test_total_time'))
    count_failed = available_data.filter(Q(result__contains='FAIL')).count()
    max_time = available_data.aggregate(Max('test_total_time'))
    max_tests = available_data.aggregate(Max('number_of_test'))

    context = {'project': project, 'data': available_data, 'pk': pk, 'names': distinct_names, 'sfcodes': distinct_sf_codes, 'family': distinct_family,
                'test_results': distinct_results, 'group_fail': distinct_fail, 'last_name': last_name, 'last_sf_code': last_sf_code, 'last_family': last_family,
                'last_result': last_result, 'last_fail': last_fail, 'filter_active': filter_active, 'test_total': test_total, 'count_failed': count_failed,
                'max_time': max_time, 'max_tests': max_tests}

    if permission==False:
        visitor = Visitor.objects.get(id=request.user.id)
        field_object = Visitor._meta.get_field('visible_test_projects')
        available_projects = field_object.value_from_object(visitor)

        for project in available_projects:
            if project.id == int(pk):
                print("Naslo se")
                return render(request, 'base/project_page.html', context)    
        return redirect('home')
    else:
        return render(request, 'base/project_page.html', context)

@user_passes_test(lambda u: u.is_superuser)
def create_visitor(request):
    form = VisitorForm()
    if request.method == 'POST':
        form = VisitorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/visitor_form.html', context)

@login_required(login_url='login')
def update_visitor(request, pk):
    visitor = Visitor.objects.get(id=pk)
    form = VisitorFormUpdate(instance=visitor) # davame do formulare rovnou predvyplnena data odpovidajiciho uzivatele

    if request.method == 'POST':
        form = VisitorFormUpdate(request.POST, instance=visitor)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/visitor_form.html', context)

@user_passes_test(lambda u: u.is_superuser)
def create_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.host = request.user
            project.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/testproject_form.html', context)

@user_passes_test(lambda u: u.is_superuser)
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

@user_passes_test(lambda u: u.is_superuser)
def delete_project(request, pk):
    project = Test_project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'object': project})

@user_passes_test(lambda u: u.is_superuser)
def delete_visitor(request, pk):
    visitor = Visitor.objects.get(id=pk)
    if request.method == 'POST':
        visitor.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'object': visitor})

@user_passes_test(lambda u: u.is_superuser)
def list_visitors(request):

    search_user = request.GET.get('search_user') if request.GET.get('search_user') != None else ''
    
    visitors = Visitor.objects.all()

    if search_user != '':
        visitors = Visitor.objects.filter(first_name__regex=r'^'+search_user+'.*')
    
    context = {'visitors': visitors}
    #print(visitors.visible_test_projects.all())
    return render(request, 'base/see_visitors.html', context)

@login_required(login_url='login')
def show_profile(request, pk):
    if request.user.is_superuser == False:
        visitor = Visitor.objects.get(id=pk)
        form = VisitorFormUser(instance=visitor) # davame do formulare rovnou predvyplnena data odpovidajiciho uzivatele

        if request.method == 'POST':
            form = VisitorFormUser(request.POST, instance=visitor)
            if form.is_valid():
                form.save()
                return redirect('home')

        if request.user.id != int(pk):
            return redirect('home')

        context = {'form': form}
        return render(request, 'base/visitor_form.html', context)
    else:
        user = User.objects.get(id=pk)
        form = VisitorFormUser(instance=user) # davame do formulare rovnou predvyplnena data odpovidajiciho uzivatele

        if request.method == 'POST':
            form = VisitorFormUser(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('home')

        context = {'form': form}
        return render(request, 'base/visitor_form.html', context)



@user_passes_test(lambda u: u.is_superuser)
def upload_data(request, pk):
    form = UploadFileForm
    if request.method == 'POST':

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filename = str(request.FILES['file'])
            print(request.FILES['file'])
            print(dir(request.FILES['file']))
            case = Test_project.objects.get(id=pk)
            load_file(filename, request.FILES['file'], case)

            print('POST and valid')
            return redirect('project', pk=pk)

    context = {'form': form}
    return render(request, 'base/upload_data.html', context)



    



