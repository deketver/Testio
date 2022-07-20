from django.contrib import admin
from .models import Test_project, Visitor, High_level_tests 

# Register your models here.

admin.site.register(High_level_tests)
admin.site.register(Test_project)
admin.site.register(Visitor)