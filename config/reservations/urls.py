from django.urls import path

from .views import (
    ReservationCreateView,
    MyReservationListView,
    ReservationDetailView,
    CancelReservationView,
    AdminReservationListView,
    AdminReservationStatusView,
)


urlpatterns = [

    # Customer
    path(
        "reservations/",
        ReservationCreateView.as_view(),
        name="reservation-create"
    ),

    path(
        "reservations/my/",
        MyReservationListView.as_view(),
        name="my-reservations"
    ),

    path(
        "reservations/<int:pk>/",
        ReservationDetailView.as_view(),
        name="reservation-detail"
    ),

    path(
        "reservations/<int:pk>/cancel/",
        CancelReservationView.as_view(),
        name="reservation-cancel"
    ),

    # Admin
    path(
        "admin/reservations/",
        AdminReservationListView.as_view(),
        name="admin-reservations"
    ),

    path(
        "admin/reservations/<int:pk>/status/",
        AdminReservationStatusView.as_view(),
        name="admin-reservation-status"
    ),
]