from rest_framework import serializers
from .models import Car
from .models import Employee
from .models import Customer

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'make', 'carmodel', 'year', 'location', 'status']
        
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'age', 'address', 'branch'] 
        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        field = ['id','name', 'age', 'address', 'cars']