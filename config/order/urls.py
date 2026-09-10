
from django.urls import path

from .views import (
    OrderCreateView,
    MyOrdersView,
    CancelOrderView
)


urlpatterns = [

    path('create-order/',OrderCreateView.as_view(), name='create-order'),
    path('my-orders/',MyOrdersView.as_view(),name='my-orders'),
    path('<int:pk>/cancel/',CancelOrderView.as_view(), name='cancel-order'),

]