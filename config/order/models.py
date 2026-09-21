from django.db import models
from django.conf import settings
from menu.models import MenuItem, MenuItemCustomization
class Order(models.Model):
     STATUS_CHOICES = [('PENDING', 'Pending'),('CONFIRMED', 'Confirmed'),
                       ('PREPARING', 'Preparing'),('READY', 'Ready'),
                       ('COMPLETED', 'Completed'),('CANCELLED', 'Cancelled'),
    ]
     user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='orders')
     status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='PENDING')
     total_amount=models.DecimalField( max_digits=10,decimal_places=2,default=0)
     created_at=models.DateTimeField(auto_now_add=True)
     updated_at=models.DateTimeField(auto_now=True)


     def __str__(self):
        return f"Order #{self.id}-{self.user.username}"

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    related_name='items'
    menu_item = models.ForeignKey(MenuItem,on_delete=models.PROTECT,related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField( max_digits=10,decimal_places=2)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.menu_item.name}-{self.quantity}"


class OrderItemCustomization(models.Model):

    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE,related_name='customizations')
    customization = models.ForeignKey(MenuItemCustomization,on_delete=models.PROTECT, related_name='order_customizations')

    # Order time customization  price
    price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.customization.name}"    
    





# Create your models here.
