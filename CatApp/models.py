from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save

# Create your models here.
class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_catering = models.BooleanField(default=False)

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=10,null=True)
    customer_name = models.CharField(max_length=10,null=True)
    gender_choices = [('M', 'Male'), ('F', 'Female')]
    gender = models.CharField(choices=gender_choices,max_length=1,default=None,null=True)
    phone = models.CharField(max_length=10,blank=False)
    address = models.TextField()

    def __str__(self):
        return self.user.username

class Catering(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    catering_name = models.CharField(max_length=100,blank=False)
    about_info = models.CharField(max_length=100,blank=False)
    location = models.CharField(max_length=40,blank=False)
    logo = models.FileField(blank=False)
    approved = models.BooleanField(blank=False,default=True)

    def __str__(self):
        return self.catering_name

class Menu(models.Model):
    owner = models.ForeignKey(Catering,on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100,blank=False)
    price = models.IntegerField(blank=False)
    quantity = models.IntegerField(blank=False,default=0)

    def __str__(self):
       return self.item_name+' - '+str(self.price)

class Bill(models.Model):
    id = models.AutoField(primary_key=True)
    total_amount = models.IntegerField(blank=True,null=True)
    time = models.DateTimeField(auto_now_add=True)
    event_name = models.CharField(max_length=100,blank=False)
    event_location =  models.CharField(max_length=100,blank=False)
    orderedBy = models.ForeignKey(User,on_delete=models.CASCADE)
    number_of_people = models.IntegerField(blank=True,null=True)
    owner = models.ForeignKey(Catering,on_delete=models.CASCADE)

    BOOKING_PENDING = "Pending"
    BOOKING_ACCEPTED = "Accepted"
    BOOKING_REJECTED = "Rejected"

    BOOKING_CHOICES = (
        (BOOKING_PENDING, BOOKING_PENDING),
        (BOOKING_ACCEPTED, BOOKING_ACCEPTED),
        (BOOKING_REJECTED, BOOKING_REJECTED)
    )
    status = models.CharField(max_length=20,null=True,choices= BOOKING_CHOICES,default=BOOKING_PENDING)
    

    def __str__(self):
        return str(self.id) +' '+str(self.status)

class orderItem(models.Model):
    id          = models.AutoField(primary_key=True)
    item_id     = models.ForeignKey(Menu ,on_delete=models.CASCADE)
    bill_id      = models.ForeignKey(Bill,on_delete=models.CASCADE)
    quantity    = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.id)  










        




