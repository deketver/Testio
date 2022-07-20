from django.forms import ModelForm
from django import forms
from .models import Test_project, Visitor
from django.contrib.auth.forms import UserCreationForm

class VisitorForm(ModelForm):
    class Meta:
        model = Visitor
        projects = Test_project.objects.all()
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'user_permissions', 'is_visitor', 'visible_test_projects']
    #projects = forms.MultipleChoiceField(queryset=Test_project.objects.all())

class ProjectForm(ModelForm):
    class Meta:
        model = Test_project
        fields = '__all__'