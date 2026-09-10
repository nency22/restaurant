from rest_framework import serializers

from .models import (
    Order,
    OrderItem,
    OrderItemCustomization
)




class OrderItemCustomizationSerializer(serializers.ModelSerializer):

    customization_name = serializers.CharField(
        source='customization.name',
        read_only=True
    )

    class Meta:
        model = OrderItemCustomization

        fields = [
            'id',
            'customization',
            'customization_name',
            'price',
        ]

        read_only_fields = [
            'price',
        ]


class OrderItemSerializer(serializers.ModelSerializer):

    menu_item_name = serializers.CharField(
        source='menu_item.name',
        read_only=True
    )

    customizations = OrderItemCustomizationSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = OrderItem

        fields = [
            'id',
            'menu_item',
            'menu_item_name',
            'quantity',
            'price',
            'subtotal',
            'customizations',
        ]

        read_only_fields = [
            'price',
            'subtotal',
        ]


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Order

        fields = [
            'id',
            'user',
            'status',
            'total_amount',
            'created_at',
            'updated_at',
            'items',
        ]

        read_only_fields = [
            'user',
            'status',
            'total_amount',
            'created_at',
            'updated_at',
        ]

class OrderCreateItemSerializer(serializers.Serializer):

    menu_item = serializers.IntegerField()

    quantity = serializers.IntegerField(
        min_value=1
    )

    customizations = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        default=[]
    )


class OrderCreateSerializer(serializers.Serializer):

    items = OrderCreateItemSerializer(
        many=True
    )

    def validate_items(self, value):

        if not value:
            raise serializers.ValidationError(
                "Order must contain at least one item."
            )

        return value        