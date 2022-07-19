from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name="home"),
    path('', views.login_page, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('create_visitor/', views.create_visitor, name='create_visitor')
    
]
