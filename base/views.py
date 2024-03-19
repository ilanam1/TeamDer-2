from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import User
from .models import loginUser
#from .forms import UserSignUpForm

# Create your views here.
def Home(request):
    return render(request,'base/homePage.html')
'''
def register(request):

    if request.method=='POST':
        form=UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('base/signUp.html')
    else:
        form=UserSignUpForm()
    return render(request,'base/signUp.html',{'form':form})
'''

def register(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name = request.POST['last_name']
        gender=request.POST['gender']
        degree=request.POST['degree']
        birth_day=request.POST['birth_date']
        email=request.POST['email']
        password=request.POST['password']



        newUser=User(first_name=first_name,last_name=last_name,gender=gender,degree=degree,
                     birth_day=birth_day,email=email,password=password)

        newUser.save()
        return redirect('/register/')

    context={}
    return render(request,'base/signUp.html',context)



def login(request):
    if request.method=='POST':
        userName=request.post['email']
        password=request.post['password']
    loginU=loginUser(userName=userName,password=password)
    loginU.save()
    return render(request,'sighIn.html')


