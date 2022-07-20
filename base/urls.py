from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name="home"),
    path('', views.login_page, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('create_visitor/', views.create_visitor, name='create_visitor'),
    path('update_visitor/<str:pk>/', views.update_visitor, name='update_visitor'),
    path('delete_visitor/<str:pk>/', views.delete_visitor, name='delete_visitor'),
    path('create_project/', views.create_project, name='create_project'),
    path('update_project/<str:pk>/', views.update_project, name='update_project'),
    path('delete_project/<str:pk>/', views.delete_project, name='delete_project'),
    path('project/<str:pk>/', views.project, name='project'),
    path('list_users/', views.list_visitors, name='list_visitors'),
    path('user_profile/<str:pk>/', views.show_profile, name='show_profile'),
    path('upload_data/<str:pk>/', views.upload_data, name='upload_data'),
    
]
