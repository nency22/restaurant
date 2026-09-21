from rest_framework import serializers

from .models import Table, Reservation
from .validators import (
    validate_reservation_datetime,
    validate_guest_count,
)


class TableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Table

        fields = [
            "id",
            "table_number",
            "capacity",
            "is_active",
        ]

        read_only_fields = [
            "id",
        ]


class ReservationSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(
        read_only=True
    )

    table_number = serializers.IntegerField(
        source="table.table_number",
        read_only=True
    )

    class Meta:
        model = Reservation

        fields = [
            "id",
            "user",
            "table",
            "table_number",
            "reservation_date",
            "reservation_time",
            "number_of_guests",
            "special_request",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "table",
            "table_number",
            "status",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):

        reservation_date = attrs[
            "reservation_date"
        ]

        reservation_time = attrs[
            "reservation_time"
        ]

        number_of_guests = attrs[
            "number_of_guests"
        ]

        validate_reservation_datetime(
            reservation_date,
            reservation_time
        )

        validate_guest_count(
            number_of_guests
        )

        return attrs