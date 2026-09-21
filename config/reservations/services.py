from django.db import transaction
from django.db.models import Exists, OuterRef

from rest_framework.exceptions import ValidationError

from .models import Table, Reservation


@transaction.atomic
def create_reservation(
    *,
    user,
    reservation_date,
    reservation_time,
    number_of_guests,
    special_request=""
):

    reserved_tables = Reservation.objects.filter(
        table=OuterRef("pk"),
        reservation_date=reservation_date,
        reservation_time=reservation_time,
        status__in=[
            Reservation.Status.PENDING,
            Reservation.Status.CONFIRMED,
        ],
    )

    table = (
        Table.objects
        .select_for_update()
        .filter(
            is_active=True,
            capacity__gte=number_of_guests,
        )
        .annotate(
            is_reserved=Exists(reserved_tables)
        )
        .filter(
            is_reserved=False
        )
        .order_by(
            "capacity",
            "table_number"
        )
        .first()
    )

    if table is None:
        raise ValidationError(
            {
                "reservation": (
                    "No suitable table is available "
                    "for the selected date, time and "
                    "number of guests."
                )
            }
        )

    reservation = Reservation.objects.create(
        user=user,
        table=table,
        reservation_date=reservation_date,
        reservation_time=reservation_time,
        number_of_guests=number_of_guests,
        special_request=special_request,
        status=Reservation.Status.PENDING,
    )

    return reservation