from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

class Posts(models.Model):

    FILE_TYPE_CHOICES = [
        (1, 'File'),
        (2, 'Folder'),
    ]
    name = models.TextField()
    image = models.TextField()
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    size = models.CharField(max_length=100)
    lang = models.TextField()
    genre = models.TextField()
    story = models.TextField()
    link = models.CharField(max_length=100)
    type = models.IntegerField(choices=FILE_TYPE_CHOICES, default=1)
    duration=models.TextField(null=True, blank=True)
    more = models.TextField()
    parent = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100)
    starcast=models.TextField()
    menu=models.TextField(null=True, blank=True)
    release_date=models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Trand(models.Model):
    post = models.ForeignKey(Posts,related_name="posts", on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Menu(models.Model):
    FILE_TYPE_CHOICES = [
        (1, 'File'),
        (2, 'Folder'),
    ]
    name = models.CharField(max_length=100)
    menuId = models.CharField(max_length=100,null=True)
    type = models.IntegerField(choices=FILE_TYPE_CHOICES, default=1)
    link = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100)


    
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

class Customer(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=255)
    profile = models.FileField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    email_verify = models.CharField(max_length=15, blank=True, null=True)
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
            customer = Customer.objects.get(email=email)
            if customer.check_password(password):
                return customer
        except Customer.DoesNotExist:
            return None
        return None

    def __str__(self):
        return self.email

class Role(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

class Roles(models.Model):
    user =  models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE,related_name='role')
    assign = models.TextField(null=True, blank=True)
    given = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='given',null=True,blank=True,default=None)
    

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
    
class Comments(models.Model):
    user =  models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='customer')
    msg = models.TextField(blank=True, null=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE,related_name='post')
    parentId = models.CharField(max_length=100,null=True)
    status = models.CharField(max_length=100,default='0')
    created = models.DateField(auto_now_add=True)


class MailMessage(models.Model):
    subject =  models.CharField(max_length=200,null=True)
    to_address = models.EmailField(max_length=100)
    from_address = models.EmailField(max_length=100)
    content =  models.TextField(blank=True, null=True)



"""
class Comments(models.Model):
    name =  models.CharField(max_length=100,null=True)
    msg = models.TextField(blank=True, null=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE,related_name='post')
    email =  models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='user')
    parentId = models.CharField(max_length=100,null=True)
    status = models.CharField(max_length=100,default='0')
    created = models.DateField(auto_now_add=True)
"""
