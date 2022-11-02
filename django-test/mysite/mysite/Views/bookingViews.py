from ..models import Car
from ..models import Customer
from rest_framework.response import Response
from ..serializers import CarSerializer
from ..serializers import CustomerSerializer
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.shortcuts import render,redirect

@api_view(['GET','PUT'])
def order_car(request, id):
    try:
        theCar = Car.objects.get(pk=id)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    
    if theCar.car_status == "available":
        serializer = CarSerializer(theCar, data=request.data)
        serializer.update(theCar, {"car_status": "booked"})
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)  
    return Response(status=status.HTTP_204_NO_CONTENT)