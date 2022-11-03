from django.db import models
from django.contrib import admin
from django.utils import timezone

class Car(models.Model):
    make = models.CharField(max_length=50)
    carmodel = models.CharField(max_length=50)
    year = models.IntegerField()
    location = models.CharField(max_length=50)
    car_status = models.CharField(max_length=50, default = "AVAILABLE")
    def __str__(self): 
        return self.make + ' ' + self.carmodel
    
class Customer(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    address = models.CharField(max_length=100)

    def __str__(self): 
        return self.name
    
class Employee(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    address = models.CharField(max_length=100)
    branch = models.CharField(max_length=50)

    def __str__(self): 
        return self.name

class Booking(models.Model):
    customer = models.IntegerField()
    car = models.IntegerField()
    booking_status = models.CharField(max_length=50, default = "BOOKED")
    
    def __str__(self):
        return str(self.customer) + "- " + str(self.car)