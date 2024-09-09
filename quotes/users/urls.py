from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signupuser, name='signup'),
    path('profile/',views.user_profile, name='user_profile'),
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name='logout'),
]
