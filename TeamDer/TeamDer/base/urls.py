from django.urls import path
from .import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('',views.Home,name="home"),
    path('register/',views.register,name="register"),
    path('login/',views.login,name="login"),

    path('Home/',views.Home,name="Home"),
    path('bioAndPhoto/',views.bioAndPhoto,name="bioAndPhoto"),
    path('userHomePage/',views.userHomePage,name="userHomePage"),
    path('FindFriends/', views.FindFriends, name='FindFriends'),
    path('dikanatPage/', views.dikanatPage, name='dikanatPage'),
    path('profile/', views.profile, name='profile'),
    path('users_slider/', views.users_slider, name='users_slider'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('send_friend_request/', views.send_friend_request, name='send_friend_request'),
    path('friend_requests/', views.friend_requests, name='friend_requests'),
    path('accept_request/', views.accept_friend_request, name='accept_request'),
    path('reject_request/', views.decline_friend_request, name='reject_request'),
    path('logout/',  auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('studyGroupsPage/',views.studyGroupsPage,name='studyGroupsPage'),
    path('submit_questionnaire/', views.submit_questionnaire, name='submit_questionnaire'),
    path('questionnariePage', views.questionnariePage, name='questionnariePage'),
    path('my_view',views.my_view,name='my_view'),
    path('confirm_delete/', views.confirm_delete, name='confirm_delete'),





]