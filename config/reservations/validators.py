from datetime import datetime

from django.utils import timezone
from rest_framework import serializers


def validate_reservation_datetime(
    reservation_date,
    reservation_time
):
    naive_datetime = datetime.combine(
        reservation_date,
        reservation_time
    )

    reservation_datetime = timezone.make_aware(
        naive_datetime,
        timezone.get_current_timezone()
    )

    if reservation_datetime <= timezone.now():
        raise serializers.ValidationError(
            "Reservation date and time must be in the future."
        )


def validate_guest_count(number_of_guests):
    if number_of_guests <= 0:
        raise serializers.ValidationError(
            "Number of guests must be greater than zero."
        )

    if number_of_guests > 20:
        raise serializers.ValidationError(
            "Maximum 20 guests are allowed per reservation."
        )