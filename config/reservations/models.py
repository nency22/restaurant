from django.conf import settings
from django.db import models


class Table(models.Model):
    table_number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["table_number"]

    def __str__(self):
        return f"Table {self.table_number}"


class Reservation(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    table = models.ForeignKey(
        Table,
        on_delete=models.PROTECT,
        related_name="reservations"
    )

    reservation_date = models.DateField()
    reservation_time = models.TimeField()

    number_of_guests = models.PositiveIntegerField()

    special_request = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-reservation_date", "-reservation_time"]

        indexes = [
            models.Index(
                fields=[
                    "reservation_date",
                    "reservation_time",
                    "status"
                ]
            ),
            models.Index(
                fields=[
                    "table",
                    "reservation_date",
                    "reservation_time"
                ]
            ),
        ]

    def __str__(self):
        return (
            f"Reservation #{self.id} - "
            f"Table {self.table.table_number}"
        )