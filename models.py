from django.db import models
from django.contrib.auth.models import User
# Create your models here.


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class custumeUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    gender = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    birth_day = models.DateField()
    password = models.CharField(max_length=100)
    last_login = models.DateTimeField(auto_now=True)


    summary = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default_images/default_profile_pic.jpg')

    # Add your additional fields here

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

'''
class custumeUser(models.Model):
    first_name=models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    birth_day=models.DateField()
    email = models.EmailField(max_length=100)
    password= models.CharField(max_length=100)

    def __str__(self):
        return self.email
'''


class loginUser(models.Model):
    userName = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.userName



class friends(models.Model):
    '''
          Keturah Shlomo's model
    '''
    userName = models.EmailField(max_length=100)
    friend = models.ForeignKey(custumeUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default="")
    objects = models.Manager()
