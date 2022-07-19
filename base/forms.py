from django.forms import ModelForm
from .models import Test_project, Visitor

class VisitorForm(ModelForm):
    class Meta:
        model = Visitor
        fields = '__all__'

class ProjectForm(ModelForm):
    class Meta:
        model = Test_project
        fields = '__all__'