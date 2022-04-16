from django.db import models
from django.db.models.enums import Choices
from django.db.models.fields.json import DataContains

# Create your models here.

class Appointment(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    request = models.TextField(blank=True)
    req_date = models.DateField(auto_now_add=True)   #date patient sent req in
    accepted = models.BooleanField(default=False)    # date that was accenpted by admin
    accepted_date = models.DateField(auto_now_add=True, null=False, blank=False)  # to see accept or reject status of request
    
    # displaying name of patient to the admin panel
    def __str__(self):
        return self.fname

    # displaying requested date
    class Meta:
        ordering = ["-req_date"]

#for patient signup
class Patient(models.Model):
    name=models.CharField(max_length=80)
    email=models.EmailField(unique=True)
    gender=models.CharField(max_length=10)
    phonenumber=models.CharField(max_length=16)
    address=models.CharField(max_length=200)
    birthdate=models.DateField()
    bloodgroup= models.CharField(max_length=10)

         



