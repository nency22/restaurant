from django.contrib import admin
from .models import Category, MenuItem,MenuItemCustomization
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(MenuItemCustomization)

# Register your models here.
