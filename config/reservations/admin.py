from django.contrib import admin

from .models import Table, Reservation


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "table_number",
        "capacity",
        "is_active",
    ]

    list_filter = [
        "is_active",
    ]


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "user",
        "table",
        "reservation_date",
        "reservation_time",
        "number_of_guests",
        "status",
    ]

    list_filter = [
        "status",
        "reservation_date",
    ]

    search_fields = [
        "user__username",
        "user__email",
    ]