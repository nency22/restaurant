from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import  Reservation
from .serializers import (
    
    ReservationSerializer,
)
from .permissions import IsAdminRole
from .services import create_reservation


class ReservationCreateView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        serializer = ReservationSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        reservation = create_reservation(
            user=request.user,
            reservation_date=serializer.validated_data[
                "reservation_date"
            ],
            reservation_time=serializer.validated_data[
                "reservation_time"
            ],
            number_of_guests=serializer.validated_data[
                "number_of_guests"
            ],
            special_request=serializer.validated_data.get(
                "special_request",
                ""
            ),
        )

        response_serializer = ReservationSerializer(
            reservation
        )

        return Response(
            {
                "message": "Reservation created successfully.",
                "data": response_serializer.data,
            },
            status=status.HTTP_201_CREATED
        )
class MyReservationListView(APIView):

      permission_classes = [
          IsAuthenticated
        ]

      def get(self, request):

        reservations = (
            Reservation.objects
            .filter(user=request.user)
            .select_related("table")
        )

        serializer = ReservationSerializer(
            reservations,
            many=True
        )

        return Response(
            serializer.data
        )

class ReservationDetailView(APIView):

       permission_classes = [
        IsAuthenticated
      ]

       def get(self, request, pk):

        try:

            reservation = (
                Reservation.objects
                .select_related("table")
                .get(
                    pk=pk,
                    user=request.user
                )
            )

        except Reservation.DoesNotExist:

            return Response(
                {
                    "message": "Reservation not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ReservationSerializer(
            reservation
        )

        return Response(
            serializer.data
        )
class CancelReservationView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def patch(self, request, pk):

        try:

            reservation = Reservation.objects.get(
                pk=pk,
                user=request.user
            )

        except Reservation.DoesNotExist:

            return Response(
                {
                    "message": "Reservation not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if reservation.status in [
            Reservation.Status.COMPLETED,
            Reservation.Status.CANCELLED,
        ]:

            return Response(
                {
                    "message": (
                        "This reservation cannot "
                        "be cancelled."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        reservation.status = (
            Reservation.Status.CANCELLED
        )

        reservation.save(
            update_fields=[
                "status",
                "updated_at"
            ]
        )

        return Response(
            {
                "message": (
                    "Reservation cancelled successfully."
                )
            }
        )
class AdminReservationListView(APIView):

    permission_classes = [
        IsAdminRole
    ]

    def get(self, request):

        reservations = (
            Reservation.objects
            .select_related(
                "user",
                "table"
            )
            .all()
        )

        serializer = ReservationSerializer(
            reservations,
            many=True
        )

        return Response(
            serializer.data
        )
class AdminReservationStatusView(APIView):

    permission_classes = [
        IsAdminRole
    ]

    def patch(self, request, pk):

        try:

            reservation = Reservation.objects.get(
                pk=pk
            )

        except Reservation.DoesNotExist:

            return Response(
                {
                    "message": "Reservation not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        new_status = request.data.get(
            "status"
        )

        allowed_transitions = {
            Reservation.Status.PENDING: [
                Reservation.Status.CONFIRMED,
                Reservation.Status.CANCELLED,
            ],

            Reservation.Status.CONFIRMED: [
                Reservation.Status.COMPLETED,
                Reservation.Status.CANCELLED,
            ],

            Reservation.Status.COMPLETED: [],

            Reservation.Status.CANCELLED: [],
        }

        current_status = reservation.status

        if new_status not in allowed_transitions.get(
            current_status,
            []
        ):

            return Response(
                {
                    "message": (
                        f"Cannot change status from "
                        f"{current_status} to "
                        f"{new_status}."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        reservation.status = new_status

        reservation.save(
            update_fields=[
                "status",
                "updated_at"
            ]
        )

        return Response(
            {
                "message": (
                    "Reservation status updated successfully."
                ),
                "status": reservation.status,
            }
        )        