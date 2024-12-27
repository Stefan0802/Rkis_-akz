from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Userprofile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    middle_name = models.CharField(max_length=100, blank=False, null=False)
    avatar = models.ImageField(upload_to="avatar/", blank=True, null=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=250, blank=False, null=False)
    description = models.CharField(max_length=300, blank=True, null=True)
    number = models.IntegerField( blank=False, null=False)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.title