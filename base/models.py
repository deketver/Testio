from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class Xml_Files(models.Model):
#     unique_id = models.CharField(max_length=400, blank=False, unique=True)
#     name = models.CharField(max_length=300)
#     sf_code = models.CharField(max_length=300) #identifikator typu produktu
#     family = models.CharField(max_length=200)
#     sf_sn = models.CharField(max_length=200,  blank=True)  #seriove cislo short
#     si_id_string = models.CharField(max_length=200, null=True, blank=True) #seriove cislo full
#     result = models.CharField(max_length=200)
#     fail_test_name = models.CharField(max_length=300,default='', null=True, blank=True)
#     fail_group_name = models.CharField(max_length=200,default='', null=True, blank=True)
#     test_total_time = models.IntegerField()
#     tester_info = models.CharField(max_length=200,  blank=True) #nazev testovaci aplikace a jeji cislo
#     user_name = models.CharField(max_length=200,  blank=True) #uzivatel z vyrobniho zavodu
#     timestamp = models.DateTimeField() #example "2022-03-01 00:39:50.8" - bude asi prevest na datetime z isoformatu
#     ini_security = models.CharField(max_length=300,  blank=True) #unikatni security 
#     number_of_test = models.IntegerField(default=0,  blank=True)  #pocet souboru v ramci test scenario

#     def __str__(self):
#         return self.unique_id



class Test_project(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) #nekdo musi hostovat dany room
    name = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True) #muze to byt ponechano prazdne, a pak i po editu
    #allowed_users = models.ManyToManyField(User)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

class Visitor(User):
    # creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_creator') #nekdo musi hostovat daneho ciloveho uzivatele
     is_visitor = models.BooleanField(default=False)
     visible_test_projects = models.ManyToManyField(Test_project)

     def __str__(self) -> str:
         return super().__str__()

# class Visitor(models.Model):
#      user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#      test_group = models.ManyToManyField(Test_project)


class High_level_tests(models.Model):
     project = models.ForeignKey(Test_project, on_delete=models.CASCADE)
     unique_id = models.CharField(max_length=400, blank=False)
     unique_id_sequence = models.CharField(max_length=400, blank=False, unique=True)
     title = models.CharField(max_length=400, blank=False)
     test_class = models.CharField(max_length=400, blank=True)
     retest = models.CharField(max_length=200, blank=True)
     test_result = models.CharField(max_length=200)

     def __str__(self):
        return self.unique_id_sequence