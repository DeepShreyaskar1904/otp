# from django.contrib import admin
# from django.urls import path,include
# from .views import *
#
# from . import views
# urlpatterns = [
#     path('',views.reg,name='reg'),
#     path('success/',views.success,name='success'),
#     path("dash/",views.dash,name='dash'),
#     path('update/<int:id>/', views.update_user, name='update_user'),
#     path('delete/<int:id>/', views.delete_user, name='delete_user'),
#     path('verify-otp/', views.verify_otp, name='verify_otp'),
#     path('login/',views.login_view,name="login")
#
# ]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # Default page = login
    path('register/', views.reg, name='reg'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('dash/', views.dash, name='dash'),
    path('logout/', views.logout_view, name='logout'),
    path('update/<int:id>/', views.update_user, name='update_user'),
    path('delete/<int:id>/', views.delete_user, name='delete_user'),
    path('success/', views.success, name='success'),
]