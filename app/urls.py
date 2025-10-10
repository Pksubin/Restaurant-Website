from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('menu/', views.menu, name='menu'),
    path('reservation/', views.reservation, name='reservation'),
    path('contact/', views.contact, name='contact'),
   
     path('admin-login/', views.admin_login, name='admin-login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('admin-logout/', views.admin_logout, name='admin-logout'),
    
    
]