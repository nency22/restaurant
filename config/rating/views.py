from django.db.models import Avg, Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from .models import Rating
from .serializers import RatingSerializer

from menu.models import MenuItem
from order.models import Order


class RatingListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=RatingSerializer,
        responses=RatingSerializer
    )
    def post(self, request):

        menu_item_id = request.data.get('menu_item')

        # Check menu item
        try:
            menu_item = MenuItem.objects.get(
                id=menu_item_id
            )
        except MenuItem.DoesNotExist:
            return Response(
                {
                    "message": "Menu item not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Check completed order
        completed_order = Order.objects.filter(
            user=request.user,
            status='COMPLETED',
            items__menu_item=menu_item
        ).exists()

        if not completed_order:
            return Response(
                {
                    "message": "You can rate this item only after completing an order."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # Check existing rating
        existing_rating = Rating.objects.filter(
            user=request.user,
            menu_item=menu_item
        ).first()

        if existing_rating:
            return Response(
                {
                    "message": "You have already rated this menu item."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RatingSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                user=request.user
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request):

        menu_item_id = request.query_params.get(
            'menu_item'
        )

        if not menu_item_id:
            return Response(
                {
                    "message": "menu_item is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        ratings = Rating.objects.filter(
            menu_item_id=menu_item_id
        )

        serializer = RatingSerializer(
            ratings,
            many=True
        )

        return Response(
            serializer.data
        )
class RatingDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        try:
            return Rating.objects.get(pk=pk)

        except Rating.DoesNotExist:
            return None

    @extend_schema(
        request=RatingSerializer,
        responses=RatingSerializer
    )
    def patch(self, request, pk):

        rating = self.get_object(pk)

        if rating is None:
            return Response(
                {
                    "message": "Rating not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Only owner can update
        if rating.user != request.user:
            return Response(
                {
                    "message": "You can update only your own rating."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = RatingSerializer(
            rating,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):

        rating = self.get_object(pk)

        if rating is None:
            return Response(
                {
                    "message": "Rating not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Only owner can delete
        if rating.user != request.user:
            return Response(
                {
                    "message": "You can delete only your own rating."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        rating.delete()

        return Response(
            {
                "message": "Rating deleted successfully"
            },
            status=status.HTTP_204_NO_CONTENT
        )
class RatingSummaryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, menu_item_id):

        ratings = Rating.objects.filter(
            menu_item_id=menu_item_id
        )

        summary = ratings.aggregate(
            average_rating=Avg('rating'),
            total_ratings=Count('id')
        )

        return Response({
            "menu_item": menu_item_id,
            "average_rating": round(
                summary['average_rating'] or 0,
                2
            ),
            "total_ratings": summary['total_ratings']
        })        