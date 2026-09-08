from django.urls import path


from .views import (
    CategoryListCreateView,
    CategoryDetailView,
    MenuListCreateView,
    MenuDetailView,
    CustomizationListCreateView,
    CustomizationDetailView
)


urlpatterns = [

    # Category
    path(
        'categories/',
        CategoryListCreateView.as_view(),
        name='category-list-create'
    ),

    path(
        'categories/<int:pk>/',
        CategoryDetailView.as_view(),
        name='category-detail'
    ),


    # Menu
    path(
        'menu/',
        MenuListCreateView.as_view(),
        name='menu-list-create'
    ),

    path(
        'menu/<int:pk>/',
        MenuDetailView.as_view(),
        name='menu-detail'
    ),


    # Customization
    path(
        'menu/<int:menu_item_id>/customizations/',
        CustomizationListCreateView.as_view(),
        name='customization-list-create'
    ),

    path(
        'customizations/<int:pk>/',
        CustomizationDetailView.as_view(),
        name='customization-detail'
    ),

     
]