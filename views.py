from django.shortcuts import render, redirect
from django.http import HttpResponse


from .models import custumeUser
from .models import friends
from django.contrib.auth.models import User
from .models import loginUser
from django.http import HttpResponse
from django.contrib.auth import authenticate as django_authenticate, login as django_login


# from .forms import UserSignUpForm

# Create your views here.
def Home(request):
    context = {}
    return render(request, 'base/homePage.html', context)


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
            request.session['user_email'] = user.email
            return redirect('/userHomePage/')
        except custumeUser.DoesNotExist:
            return render(request, 'base/sighIn.html', {'error_message': 'המשתמש אינו קיים במערכת'})

    return render(request, 'base/sighIn.html', {})


def bioAndPhoto(request):
    context = {}
    if request.method == 'POST':
        user_email = request.session.get('user_email')
        user = custumeUser.objects.get(email=user_email)
        context['user'] = user
        bio = request.POST['bio']
        profile_pic = request.FILES['profile-pic']

        if profile_pic:
            user.profile_pic = profile_pic
        user=custumeUser(summary=bio,profile_pic=profile_pic)
        user.save()
        return redirect('/login/')
    return render(request, 'base/photo_and_summary.html',context)


def b(request):
    if request.method == 'POST':
        # אין צורך לשלוף את כתובת הדוא"ל מהבקשה
        user_email = request.session.get('user_email')
        try:
            user = custumeUser.objects.get(email=user_email)
        except custumeUser.DoesNotExist:
            # אם המשתמש לא נמצא, אפשר להחזיר הודעת שגיאה או להפנות אותו לדף אחר
            # לדוגמה, דף התחברות או הרשמה
            return redirect('login_url')  # השתמש בשם ה-URL המתאים לדף ההתחברות/הרשמה שלך

        # איסוף נתוני הטופס
        bio = request.POST.get('bio')
        profile_pic = request.FILES.get('profile-pic')

        # עדכון התקציר ותמונת הפרופיל
        user.summary = bio
        if profile_pic:
            user.profile_pic = profile_pic

        # שמירת השינויים במסד הנתונים
        user.save()

        # הפניה לדף הבית של המשתמש לאחר העדכון
        return redirect('/userHomePage/')  # הפניה לדף הבית של המשתמש

    # הצגת הטופס במקרה של בקשת GET
    return render(request, 'base/photo_and_summary.html')


def userHomePage(request):
    context = {}
    user_email = request.session.get('user_email')
    user = custumeUser.objects.get(email=user_email)
    context['user'] = user
    return render(request, 'base/user_home_page.html', context)



def friend_requests(request):
    '''
    Keturah Shlomo's function
    '''
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
    '''
       Keturah Shlomo's function
    '''
    today = date.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))


def users_slider(request):
    '''
       Keturah Shlomo's function
    '''
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
    '''
       Keturah Shlomo's function
    '''
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
    '''
       Keturah Shlomo's function
    '''
    context = {}
    return render(request, 'base/FindFriends.html', context)


def dikanatPage(request):
    context = {}
    return render(request, 'base/dikanatPage.html', context)

def profile(request):
    '''
          Keturah Shlomo's function
    '''
    context = {}
    user_email = request.session.get('user_email')
    user = custumeUser.objects.get(email=user_email)
    context['user'] = user
    return render(request, 'base/update_profile.html', context)

def send_friend_request(request):
    '''
          Keturah Shlomo's function
    '''
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
    '''
          Keturah Shlomo's function
    '''
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
    '''
          Keturah Shlomo's function
    '''
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


