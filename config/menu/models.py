from django.db import models

class Category(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True, null=True)
    is_active=models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='menu_items'
    )   
    name = models.CharField(max_length=150)

    description = models.TextField(
        blank=True,
        null=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to='menu/',
        blank=True,
        null=True
    )

    is_available = models.BooleanField(
        default=True
    )
    is_veg = models.BooleanField(
        default=True
    )

    preparation_time = models.PositiveIntegerField(
        help_text='Preparation time in minutes'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    def __str__(self):
        return self.name


class MenuItemCustomization(models.Model):

    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name='customizations'
    )
    name = models.CharField(max_length=100)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.menu_item.name} - {self.name}"



# Create your models here.
