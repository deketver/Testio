from django.forms import ModelForm
from django import forms
from .models import Test_project, Visitor
from django.contrib.auth.forms import UserCreationForm

class VisitorForm(UserCreationForm):
    class Meta:
        model = Visitor
        projects = Test_project.objects.all()
        fields = ['username', 'first_name', 'last_name', 'email', 'is_visitor', 'visible_test_projects']
    #projects = forms.MultipleChoiceField(queryset=Test_project.objects.all())

class ProjectForm(ModelForm):
    class Meta:
        model = Test_project
        fields = '__all__'
        exclude = ['host']

class VisitorFormUser(UserCreationForm):
    class Meta:
        model = Visitor
        fields = ['username', 'first_name', 'last_name', 'email']

class VisitorFormUpdate(ModelForm):
    class Meta:
        model = Visitor
        fields = ['username', 'first_name', 'last_name', 'email', 'visible_test_projects']

class UploadFileForm(forms.Form):
    file = forms.FileField()
