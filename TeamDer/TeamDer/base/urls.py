from django.urls import path
from .import views

urlpatterns=[
    path('',views.Home,name="home"),
    path('register/',views.register,name="register"),
    path('login/',views.login,name="login"),

    path('Home/',views.Home,name="Home"),
    path('bioAndPhoto/',views.bioAndPhoto,name="bioAndPhoto"),
    path('userHomePage/',views.userHomePage,name="userHomePage"),
    path('FindFriends/', views.FindFriends, name='FindFriends'),
    path('dikanatPage/', views.dikanatPage, name='dikanatPage'),
    path('users_slider/', views.users_slider, name='users_slider'),

]