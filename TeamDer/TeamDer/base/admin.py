from django.contrib import admin

# Register your models here.

from .models import custumeUser
from .models import friends



admin.site.register(custumeUser)
admin.site.register(friends)

