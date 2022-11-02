from django.db import models
from django.contrib import admin
from django.utils import timezone

class Car(models.Model):
    make = models.CharField(max_length=50)
    carmodel = models.CharField(max_length=50)
    year = models.IntegerField()
    location = models.CharField(max_length=50)
    car_status = models.CharField(max_length=50, default = "available")
    def __str__(self): 
        return self.make + ' ' + self.carmodel
    
class Customer(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    address = models.CharField(max_length=100)
    cars = models.ManyToManyField(Car)
    order = models.CharField(max_length=1000)

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
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    booking_date = models.DateField(default = timezone.now)
    return_date = models.DateField(default = timezone.now)
    booking_status = models.CharField(max_length=50, default = "booked")
    
    def __str__(self):
        return str(self.customer) + "- " + str(self.car)