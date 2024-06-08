from django.db import models
from django.contrib.auth.models import AbstractUser

import datetime

# Create your models here.
class SignUp(models.Model):
	name= models.CharField(max_length=20)
	email=models.CharField(max_length=40)
	password= models.CharField(max_length=10)
	enroll=  models.CharField(max_length=20)
	YOP=models.IntegerField()
	Gender= models.CharField(max_length=10)
	course=models.CharField(max_length=10)

class ChattingDb(models.Model):
	sender=models.CharField(max_length=20)
	reciever=models.CharField(max_length=20,default=None)
	msg=models.CharField(max_length=200)
	yop=models.IntegerField(default=0)
	msgseen= models.BooleanField(default=False)
	time=models.DateTimeField()

class Blocks(models.Model):
	user=models.CharField(max_length=20)
	blocked=models.CharField(max_length=20)
	role=models.CharField(max_length=40)
	Reason=models.CharField(max_length=50)