import json
from ..models import Car
from ..models import Customer
from ..models import Booking
from rest_framework.response import Response
from ..serializers import CarSerializer
from ..serializers import CustomerSerializer
from ..serializers import BookingSerializer
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.shortcuts import render,redirect

@api_view(['GET'])
def get_bookings(request):
    bookings = Booking.objects.all()
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def get_booking(request, booking_id):
    try:
        booking = Booking.objects.get(pk=booking_id)
    except Booking.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if serializer.is_valid():
        serializer = BookingSerializer(booking)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def order_car(request):
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        customer = serializer.validated_data.get('customer')
        car = serializer.validated_data.get('car')
        booking_status = serializer.validated_data.get('booking_status')
        try:
            theCar = Car.objects.get(pk=car)
            theCustomer = Customer.objects.get(pk=customer)
            bookingsOnCar = Booking.objects.all().filter(car=theCar.id)
            bookingsOnCustomer = Booking.objects.all().filter(customer=theCustomer.id)
            customerHasAlreadyBookedCar = False
            carIsAlreadyBooked = False
            if bookingsOnCustomer is not None:
                for booking in bookingsOnCustomer:
                    if booking.booking_status.capitalize() != 'COMPLETED':
                        customerHasAlreadyBookedCar = True
            if bookingsOnCar is not None:
                for booking in bookingsOnCar:
                    if booking.booking_status.capitalize() != 'COMPLETED':
                        carIsAlreadyBooked = True
            if customerHasAlreadyBookedCar or carIsAlreadyBooked:
                message = {"message":"The selected car is not available or the customer has already booked a car."}
                return Response(data=json.dumps(message), status=status.HTTP_400_BAD_REQUEST)
            else:
                theCar.save()
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
        except Car.DoesNotExist or Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT'])
def cancel_order_car(request):
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