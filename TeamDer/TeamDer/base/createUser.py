from .models import custumeUser
from .views import register

def createNewUser(Fn,Ln,g,d,date,em,passW):
    return custumeUser.objects.create(
        first_name=Fn,
        last_name=Ln,
        gender=g,
        degree=d,
        birth_date=date,
        email=em,
        password=passW
    )