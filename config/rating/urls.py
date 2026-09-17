from django.urls import path

from .views import (
    RatingListCreateView,
    RatingDetailView,
    RatingSummaryView
)


urlpatterns = [

    path(
        'ratinglistcreate',
        RatingListCreateView.as_view(),
        name='rating-list-create'
    ),

    path(
        'ratingdetail<int:pk>/',
        RatingDetailView.as_view(),
        name='rating-detail'
    ),

    path(
        'summary/<int:menu_item_id>/',
        RatingSummaryView.as_view(),
        name='rating-summary'
    ),
]