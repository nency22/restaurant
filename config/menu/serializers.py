from rest_framework import serializers
from .models import Category, MenuItem,MenuItemCustomization

class CategorySerializer(serializers.ModelSerializer):
     class Meta:
          model=Category
          fields='__all__'

class MenuItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuItem
        fields = '__all__'

class MenuItemCustomizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuItemCustomization
        fields = '__all__'                  
        