from django.urls import path
from .import views
from django.urls import path


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
    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('send_friend_request/', views.send_friend_request, name='send_friend_request'),
    path('friend_requests/', views.friend_requests, name='friend_requests'),
    path('accept_request/', views.accept_friend_request, name='accept_request'),
    path('reject_request/', views.decline_friend_request, name='reject_request'),


]