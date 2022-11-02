from ..models import Car
from ..models import Customer
from rest_framework.response import Response
from ..serializers import CarSerializer
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.shortcuts import render,redirect

@api_view(['GET'])
def get_cars(request):
    cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True)
    print(serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def create_car(request):
    serializer = CarSerializer(data=request.data)
    if serializer.is_valid():
        # carStatus = serializer.data.get("car_status")
        # if carStatus == "available":
        #     serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_car(request, id):
    try:
        theCar = Car.objects.get(pk=id)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    
    serializer = CarSerializer(theCar, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def delete_car(request, id):
    try:
        theCar = Car.objects.get(pk=id)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)   
    theCar.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def order_car(request, car_id, cus_id):
    #if request == 'PUT':
    #    c = 0
    #    for i in id:
    #        if i != '-':
    #            c += 1
    #        else: 
    #            break
    #    car_id = int(id[0:c])
    #    cus_id = int(id[c+1:])
        try:
            theCar = Car.objects.get(pk=car_id)
            theCustomer = Customer.objects.get(pk=cus_id)
        except Car.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)    
        if theCustomer.order == 0:
            if theCar.car_status == "available":
                serializer = CarSerializer(theCar, data=request.data)
                serializer.update(theCar, {"car_status": "booked"})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST) 
            return Response(serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','PUT'])
def cancel_order_car(request, carid, custid):
    try:
        theCar = Car.objects.get(pk=carid)
        theCustomer = Customer.objects.get(pk=custid)
    except Car.DoesNotExist or Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) 
    if theCustomer.order == carid:
        serializer = CarSerializer(theCar, data=request.data)
        serializer.update(theCar, {"car_status": "available"})
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)  
    return Response(status=status.HTTP_204_NO_CONTENT)
