from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import custumeUser
from django.contrib.auth.models import User
from .models import loginUser
from django.http import HttpResponse
from django.contrib.auth import authenticate as django_authenticate, login as django_login


#from .forms import UserSignUpForm

# Create your views here.
def Home(request):

    context={}
    return render(request,'base/homePage.html',context)


def register(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name = request.POST['last_name']
        gender=request.POST['gender']
        degree=request.POST['degree']
        birth_day=request.POST['birth_date']
        email=request.POST['email']
        password=request.POST['password']
        passwordAgain=request.POST['passwordAgain']

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




        newUser=custumeUser(first_name=first_name, last_name=last_name, gender=gender, degree=degree,
                            birth_day=birth_day, email=email, password=password)

        newUser.save()
        return redirect('/bioAndPhoto/')

    context={}
    return render(request,'base/signUp.html',context)



'''

def login(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = django_authenticate(request, email=email, password=password)
        if user is not None:
            django_login(request, user)
            return redirect('/userHomePage/')
        else:
            return render(request, 'base/sighIn.html', {'error_message': 'המשתמש אינו קיים במערכת'})

    context={}
    return render(request,'base/sighIn.html',context)
'''


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = custumeUser.objects.get(email=email, password=password)
            django_login(request, user)  # התחברות ישירות למשתמש
            return redirect('/userHomePage/')
        except custumeUser.DoesNotExist:
            return render(request, 'base/sighIn.html', {'error_message': 'המשתמש אינו קיים במערכת'})

    return render(request, 'base/sighIn.html',{})







def bioAndPhoto(request):

    context = {}
    return render(request, 'base/photo_and_summary.html', context)

def userHomePage(request):
    context = {}
    return render(request, 'base/user_home_page.html', context)






from datetime import date

def calculate_age(birthdate):
    today = date.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

'''def users_slider(request):
    users = User.objects.all()
    # Dynamically add the 'age' attribute to each user
    for user in users:
        user.age = calculate_age(user.birth_day)
    return render(request, 'FindFriends.html', {'users': users})'''


def users_slider(request):
    age_filter = request.GET.get('age')
    degree_filter = request.GET.get('degree')
    users = custumeUser.objects.all()

    if degree_filter:
        users = users.filter(degree=degree_filter)

    filtered_users = []
    for user in users:
        user_age = calculate_age(user.birth_day)
        if age_filter == '18-25' and 18 <= user_age <= 25:
            filtered_users.append(user)
        elif age_filter == '25-30' and 25 <= user_age <= 30:
            filtered_users.append(user)
        elif age_filter == '30-120' and 30 <= user_age <= 120:
            filtered_users.append(user)

    return render(request, 'base/FindFriends.html', {'users': filtered_users})


def FindFriends(request):

    context = {}
    return render(request, 'base/FindFriends.html', context)


def dikanatPage(request):

    context = {}
    return render(request, 'base/dikanatPage.html', context)


def questionnariePage(request):

    context = {}
    return render(request, 'base/questionnarie.html', context)

def chatPage(request):
    if request.method == 'POST':
        message = request.POST.get('message', '')
        response = get_response(message)
        return render(request, 'base/chatPage.html', {'message': message, 'response': response})
    return render(request, 'base/chatPage.html', {'message': None, 'response': None})

def get_response(message):
    if 'hello' in message.lower():
        return 'Hello! How can I assist you today?'
    elif 'help' in message.lower():
        return 'I can help you with general questions. Please ask away!'
    elif 'goodbye' in message.lower():
        return 'Goodbye! Have a great day!'
    else:
        return "I'm sorry, I didn't understand that. Can you please rephrase your question?"
