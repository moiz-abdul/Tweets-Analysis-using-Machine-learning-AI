from django.db import models
from django.utils import timezone

# Create your models here.

class Uzerlogin(models.Model):
    Username = models.CharField(max_length=100,blank=False,null=False)
    Email = models.EmailField(max_length=100,blank=False,null=False)
    password = models.CharField(max_length=100,blank=False,null=False)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.Username


class PasswordResetOTP(models.Model):
    User_login = models.ForeignKey(Uzerlogin,on_delete=models.CASCADE, null=True)
    OTP = models.IntegerField()
    OTP_create = models.DateTimeField(default=timezone.now)
    OTP_expire = models.DateTimeField(default=timezone.now() + timezone.timedelta(minutes=5))

    def is_expired(self):
        return timezone.now() > self.OTP_expire


class UserMessage(models.Model):
    PersonName = models.CharField(max_length=100,blank=False,null=False)
    Email = models.EmailField(max_length=100,blank=False,null=False)
    PhoneNumber = models.CharField(max_length=20)
    Message = models.TextField()

    def __str__(self):
        return f"{self.PersonName}'s message" 


