"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .Views.carViews import *
from .Views.customerViews import *
from .Views.employeeViews import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cars/", get_cars),
    path("create_car/", create_car),
    path("update_car/<int:id>", update_car),
    path("delete_car/<int:id>", delete_car),
    path("order_car/<int:id>", order_car),
    path("customers/", get_customers),
    path("create_customer/", create_customer),
    path("update_customer/<int:id>", update_customer),
    path("delete_customer/<int:id>", delete_customer),
    path("employees/", get_employees),
    path("save_employee/", save_employee),
    path("update_employee/<int:id>", update_employee),
    path("delete_employee/<int:id>", delete_employee),
]