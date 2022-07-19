from django.contrib import admin
from .models import Test_project, High_level_tests, Visitor

# Register your models here.

admin.site.register(High_level_tests)
admin.site.register(Test_project)
admin.site.register(Visitor)