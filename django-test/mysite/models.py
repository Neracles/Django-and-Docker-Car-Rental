from django.db import models
from django.contrib import admin

class Car(models.Model):
    
    #https://docs.djangoproject.com/en/4.1/ref/models/fields/#field-choices-enum-types
    class CarStatusEnum(models.TextChoices):
        AVAILABLE = 'Available'
        BOOKED = 'Booked'
        RENTED = 'Rented'
        DAMAGED = 'Damaged'
    
    rent = models.TextField(blank = True)
    make = models.CharField(max_length=50)
    carmodel = models.CharField(max_length=50)
    year = models.IntegerField()
    location = models.CharField(max_length=50)
    status = models.CharField(
        max_length = 11,
        choices=CarStatusEnum.choices(),
        default=CarStatusEnum.AVAILABLE,
    )

    def __str__(self): 
        return self.make + ' ' + self.carmodel

    def create(self):
        return self.make

    def read(self):
        return

    def update(self):
        return

    def delete(self):
        return
    
class Customer(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    address = models.CharField(max_length=100)
    cars = models.ManyToManyField(Car)

    def __str__(self): 
        return self.name
    
class Employee(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    address = models.CharField(max_length=100)
    branch = models.CharField(max_length=50)

    def __str__(self): 
        return self.name
    