from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserAccountManager(BaseUserManager):
    def create_user(self,email,username,name,password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
       # self.normalize_email will turn all case of domain to lowercase to have a unique domain throughout 
        if not username:
            raise ValueError('username is required')

        email = self.normalize_email(email)
        user = self.model(email=email,username=username, name=name,**extra_fields)

        user.set_password(password)
        user.save()
        return user 
    
    def create_superuser(self,username,email,name,password=None):
        user = self.create_user(email,username, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
    

class UserAccount(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

   # objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','username']

    objects = UserAccountManager()

    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name
    
    def __str__(self) -> str:
        return self.email