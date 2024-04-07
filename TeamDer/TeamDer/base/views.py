from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import custumeUser
from django.contrib.auth.models import User
from .models import loginUser
from .models import friends
from .models import Questionnaire
from django.http import HttpResponse
from django.contrib.auth import authenticate as django_authenticate, login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required


#from .forms import UserSignUpForm

# Create your views here.
def Home(request):

    context={}
    return render(request,'base/homePage.html',context)


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        gender = request.POST['gender']
        degree = request.POST['degree']
        birth_day = request.POST['birth_date']
        email = request.POST['email']
        password = request.POST['password']
        passwordAgain = request.POST['passwordAgain']
        summary=request.POST['summary']


        if len(password) < 8:
            return render(request, 'base/signUp.html', {'error_message': 'הסיסמה חייבת להיות באורך של לפחות 8 תווים'})

            # בדיקת אות קטנה
        if not any(char.islower() for char in password):
            return render(request, 'base/signUp.html', {'error_message': 'הסיסמה חייבת לכלול לפחות אות קטנה אחת'})

            # בדיקת אות גדולה
        if not any(char.isupper() for char in password):
            return render(request, 'base/signUp.html', {'error_message': 'הסיסמה חייבת לכלול לפחות אות גדולה אחת'})

            # בדיקת תו מיוחד
        special_characters = "!@#$%^&*()-_=+"
        if not any(char in special_characters for char in password):
            return render(request, 'base/signUp.html', {'error_message': 'הסיסמה חייבת לכלול לפחות תו מיוחד אחד'})

        if password != passwordAgain:
            return render(request, 'base/signUp.html', {'error_message': 'הסיסמה ואימות הסיסמה לא תואמים'})

        newUser = custumeUser(first_name=first_name, last_name=last_name, gender=gender, degree=degree,
                              birth_day=birth_day, email=email, password=password,summary=summary)

        newUser.save()
        return redirect('/bioAndPhoto/')

    context = {}
    return render(request, 'base/signUp.html', context)






def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = custumeUser.objects.get(email=email, password=password)
            django_login(request, user)  # התחברות ישירות למשתמש
            request.session['user_email'] = user.email
            return redirect('/userHomePage/')
        except custumeUser.DoesNotExist:
            return render(request, 'base/sighIn.html', {'error_message': 'המשתמש אינו קיים במערכת'})

    return render(request, 'base/sighIn.html', {})



def bioAndPhoto(request):

    context = {}
    return render(request, 'base/photo_and_summary.html', context)

def userHomePage(request):
    context = {}
    user_email = request.session.get('user_email')
    user = custumeUser.objects.get(email=user_email)
    context['user'] = user
    return render(request, 'base/user_home_page.html', context)

def friend_requests(request):
    context = {}
    user_email = request.session.get('user_email', None)
    requests = friends.objects.all().filter(userName=user_email, status="received request")
    get_my_friends = friends.objects.all().filter(userName=user_email, status="accepted")
    my_friends = []
    for f in get_my_friends:
        temp_user = custumeUser.objects.get(email=f.friend)
        my_friends.append(temp_user)
    context['requests'] = requests
    context['my_friends'] = set(my_friends)
    return render(request, 'base/friend_requests.html', context)

from datetime import date


def calculate_age(birthdate):
    today = date.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))


def users_slider(request):
    age_filter = request.GET.get('age', None)
    degree_filter = request.GET.get('degree', None)
    users = custumeUser.objects.all()
    user_email = request.session.get('user_email', None)
    if user_email:
        users = users.exclude(email=user_email)

    # Check for 'ללא סינון' and apply filters accordingly
    if degree_filter and degree_filter != 'no_filter':
        users = users.filter(degree=degree_filter)

    if age_filter and age_filter != 'no_filter':
        filtered_users = []
        for user in users:
            user_age = calculate_age(user.birth_day)
            if age_filter == '18-25' and 18 <= user_age <= 25:
                filtered_users.append(user)
            elif age_filter == '25-30' and 25 <= user_age <= 30:
                filtered_users.append(user)
            elif age_filter == '30-120' and 30 <= user_age <= 120:
                filtered_users.append(user)
        users = filtered_users

    return render(request, 'base/FindFriends.html', {'users': users, 'user_email': user_email})



from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib import messages



def update_profile(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        degree = request.POST['degree']
        email = request.POST['email']
        # Update the user's information
        user_email = request.session.get('user_email')
        user = custumeUser.objects.get(email=user_email)

        user.first_name = first_name
        user.last_name = last_name
        user.degree = degree
        user.email = email
        user.save()
        # messages.success(request, 'Profile updated successfully.')
        return redirect('/profile/')



def FindFriends(request):
    context = {}
    return render(request, 'base/FindFriends.html', context)


def dikanatPage(request):

    context = {}
    return render(request, 'base/dikanatPage.html', context)


def profile(request):
    context = {}
    user_email = request.session.get('user_email')
    user = custumeUser.objects.get(email=user_email)
    context['user'] = user
    return render(request, 'base/update_profile.html', context)

def send_friend_request(request):
    if request.method =='POST':
        user_email = request.session.get('user_email')
        friendRef = request.POST['email']

        user = custumeUser.objects.get(email=friendRef)
        newFriend = friends(userName=user_email, friend=user, status="sent request")
        newFriend.save()

        user1 = custumeUser.objects.get(email=user_email)
        newFriend1 = friends(userName=user.email, friend=user1, status="received request")
        newFriend1.save()
        return redirect('/userHomePage/')

def accept_friend_request(request):
    if request.method =='POST':
        user_email = request.session.get('user_email', None)
        friendRef = request.POST['email']
        user = custumeUser.objects.get(email=friendRef)

        request1 = friends.objects.get(userName=user_email, friend=user, status="received request")
        request1.status = "accepted"
        request1.save()

        user1 = custumeUser.objects.get(email=user_email)
        request2 = friends.objects.get(userName=user.email, friend=user1, status="sent request")
        request2.status = "accepted"
        request2.save()
        return redirect('/friend_requests/')

def decline_friend_request(request):
    if request.method =='POST':
        user_email = request.session.get('user_email', None)
        friendRef = request.POST['email']
        user = custumeUser.objects.get(email=friendRef)

        request1 = friends.objects.get(userName=user_email, friend=user, status="received request")
        request1.status = "rejected"
        request1.save()

        user1 = custumeUser.objects.get(email=user_email)
        request2 = friends.objects.get(userName=user.email, friend=user1, status="sent request")
        request2.status = "rejected"
        request2.save()
        return redirect('/friend_requests/')

def logout(request):
    django_logout(request)
    request.session['is_logged_in'] = False
    return redirect('/Home')  # הפנייה לדף הבית של האתר או לדף אחר על פי הצורך



def studyGroupsPage(request):
    context={}
    return render(request,'base/studygroups.html',context)



def my_view(request):
    return redirect('http://127.0.0.1:5000/')



def questionnariePage(request):

    context = {}
    return render(request, 'base/questionnarie.html', context)

def submit_questionnaire(request):
    if request.method == 'POST':
        user = request.user
        social_feelings = request.POST.get('social-feelings')
        academic_progress = request.POST.get('academic-progress')

        # שמירת הנתונים במקרה של משתמש מחובר
        questionnaire = Questionnaire(user=user, social_feelings=social_feelings, academic_progress=academic_progress)
        questionnaire.save()

        # אחרי שמירת הנתונים, החזרת קישור לדף הבית של המשתמש
        return redirect('/userHomePage')
    else:
        return HttpResponse('Method Not Allowed', status=405)



def confirm_delete(request):
    if request.method == 'GET':
        return render(request, 'base/confirm_delete.html')  # יש ליצור קובץ HTML עם אישור המחיקה

    elif request.method == 'POST':
        # מחיקת המשתמש מבסיס הנתונים
        user_email = request.session.get('user_email')
        try:
            user = custumeUser.objects.get(email=user_email)
            user.delete()
            return redirect('/Home/')  # אחרי מחיקה מוציא את המשתמש לדף הבית
        except custumeUser.DoesNotExist:
            return HttpResponse('משתמש לא נמצא')








