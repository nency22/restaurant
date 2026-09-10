from django.shortcuts import render
from decimal import Decimal
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from .models import (Order,OrderItem,OrderItemCustomization)
from .serializers import (OrderSerializer,OrderCreateSerializer)
from menu.models import (MenuItem,MenuItemCustomization)
from drf_spectacular.utils import extend_schema




# Create your views here.
class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    @extend_schema(
                request=OrderCreateSerializer,
                responses=OrderCreateSerializer)
    
    def post(self, request):

        serializer = OrderCreateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        items_data = serializer.validated_data['items']
        order = Order.objects.create(user=request.user)
        total_amount = Decimal('0.00')
        for item_data in items_data:

            menu_item_id = item_data['menu_item']
            quantity = item_data['quantity']

            customization_ids = item_data.get(
                'customizations',
                []
            )

            try:
                menu_item = MenuItem.objects.get(
                    id=menu_item_id,
                    is_available=True
                )

            except MenuItem.DoesNotExist:

                return Response(
                    {
                        'error': f'Menu item {menu_item_id} is not available.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            item_price = menu_item.price

            subtotal = item_price * quantity

            order_item = OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=quantity,
                price=item_price,
                subtotal=subtotal
            )

            for customization_id in customization_ids:

                try:
                    customization = MenuItemCustomization.objects.get(
                        id=customization_id,
                        menu_item=menu_item
                    )

                except MenuItemCustomization.DoesNotExist:

                    return Response(
                        {
                            'error': (
                                f'Customization {customization_id} '
                                f'is not valid for {menu_item.name}.'
                            )
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                OrderItemCustomization.objects.create(
                    order_item=order_item,
                    customization=customization,
                    price=customization.price
                )

                subtotal += customization.price * quantity

            order_item.subtotal = subtotal
            order_item.save()

            total_amount += subtotal

        order.total_amount = total_amount
        order.save()

        response_serializer = OrderSerializer(order)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

class MyOrdersView(APIView):

     permission_classes = [IsAuthenticated]

     def get(self, request):

        orders = Order.objects.filter(
            user=request.user
        ).order_by('-created_at')

        serializer = OrderSerializer(
            orders,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )



class CancelOrderView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        try:
            order = Order.objects.get(
                id=pk,
                user=request.user
            )

        except Order.DoesNotExist:

            return Response(
                {
                    'error': 'Order not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if order.status not in ['PENDING', 'CONFIRMED']:

            return Response(
                {
                    'error': 'This order cannot be cancelled.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = 'CANCELLED'
        order.save()

        serializer = OrderSerializer(order)

        return Response(serializer.data,status=status.HTTP_200_OK)     



