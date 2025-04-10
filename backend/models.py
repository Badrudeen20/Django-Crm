from django.db import models
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password



class Module(models.Model):
    module = models.CharField(max_length=255)
    moduleType = models.CharField(max_length=255,default=1)
    url = models.CharField(max_length=255,blank=True)
    status = models.CharField(max_length=255,default=1)
    parent_id = models.CharField(max_length=255,blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.module

class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=255)
    profile = models.FileField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    is_admin = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @staticmethod
    def authenticate(email, password):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        return None

    def __str__(self):
        return self.email

class Role(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

class Roles(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)



class Permission(models.Model):
    role = models.ForeignKey(Role,on_delete=models.CASCADE)
    modules = models.ForeignKey(Module,on_delete=models.CASCADE)
    module_parent_id = models.CharField(max_length=255,blank=True)
    permission = models.CharField(max_length=255)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.permission





