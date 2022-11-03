import json
from ..models import Car
from ..models import Customer
from ..models import Booking
from rest_framework.response import Response
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
                    if booking.booking_status.upper() != "COMPLETED":
                        customerHasAlreadyBookedCar = True
            if bookingsOnCar is not None:
                for booking in bookingsOnCar:
                    if booking.booking_status.upper() != "COMPLETED":
                        carIsAlreadyBooked = True
            if customerHasAlreadyBookedCar:
                message = {"message":"The customer has already booked a car."}
                return Response(data=json.dumps(message), status=status.HTTP_400_BAD_REQUEST)
            elif carIsAlreadyBooked:
                message = {"message":"The selected car is already booked."}
                return Response(data=json.dumps(message), status=status.HTTP_400_BAD_REQUEST)
            else:
                theCar.car_status = 'BOOKED'
                theCar.save()
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
        except Car.DoesNotExist or Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','POST'])
def cancel_order_car(request):
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        customer = serializer.validated_data.get('customer')
        car = serializer.validated_data.get('car')
        try:
            theCar = Car.objects.get(pk=car)
            theCustomer = Customer.objects.get(pk=customer)
            bookingOnCar = Booking.objects.all().filter(car=theCar.id, customer=theCustomer.id)
            
            if bookingOnCar is not None and theCar is not None and theCustomer is not None:
                # Save booking status as completed
                #bookingOnCar.update(booking_status='COMPLETED')
                # Save car status as available
                theCar.car_status = 'AVAILABLE'
                theCar.save()
                bookingOnCar.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                message = {"message":"No booking found for the given customer and car."}
                return Response(data=json.dumps(message), status=status.HTTP_400_BAD_REQUEST)
        except Car.DoesNotExist or Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','POST'])
def rent_car(request):
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        customer = serializer.validated_data.get('customer')
        car = serializer.validated_data.get('car')
        try:
            theCar = Car.objects.get(pk=car)
            theCustomer = Customer.objects.get(pk=customer)
            bookingOnCar = Booking.objects.all().filter(car=theCar.id, customer=theCustomer.id)
            
            if (bookingOnCar is not None and theCar is not None and 
                theCustomer is not None):
                # Save booking status as DELIVERED
                bookingOnCar.update(booking_status='DELIVERED')
                # Save car status as available
                theCar.car_status = 'RENTED'
                theCar.save()
                return Response(status=status.HTTP_200_OK)
            else:
                message = {"message":"No booking found for the given customer and car."}
                return Response(data=json.dumps(message), status=status.HTTP_400_BAD_REQUEST)
        except Car.DoesNotExist or Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def return_car(request, new_car_status):
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        customer = serializer.validated_data.get('customer')
        car = serializer.validated_data.get('car')
        if new_car_status.capitalize() == 'DAMAGED':
            new_booking_status = 'DAMAGED'
        else:
            new_booking_status = 'COMPLETED'
            new_car_status = 'AVAILABLE'
        try:
            theCar = Car.objects.get(pk=car)
            theCustomer = Customer.objects.get(pk=customer)
            bookingOnCar = Booking.objects.all().filter(car=theCar.id, customer=theCustomer.id)
            
            if (bookingOnCar is not None and theCar is not None and 
                theCustomer is not None):
                # Save new booking statuS
                bookingOnCar.update(booking_status=new_booking_status)
                # Save nwe car status
                theCar.car_status = new_car_status
                theCar.save()
                return Response(status=status.HTTP_200_OK)
            else:
                message = {"message":"No booking found for the given customer and car."}
                return Response(data=json.dumps(message), status=status.HTTP_400_BAD_REQUEST)
        except Car.DoesNotExist or Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)