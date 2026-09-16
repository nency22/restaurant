from django.contrib import admin
from .models import Order, OrderItem,OrderItemCustomization
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderItemCustomization)



# Register your models here.
