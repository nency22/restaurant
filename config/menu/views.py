from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from .permissions import IsAdmin
from .models import (
    Category,
    MenuItem,
    MenuItemCustomization
)

from .serializers import (
    CategorySerializer,
    MenuItemSerializer,
    MenuItemCustomizationSerializer
)

class CategoryListCreateView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]

        return [IsAdmin()]

    def get(self,request):
        categories=Category.objects.all()
        serializer=CategorySerializer(categories,many=True)
        return Response(serializer.data)

    @extend_schema(
        request=CategorySerializer,
        responses=CategorySerializer
    )
    def post(self,request):
        serializer=CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
class CategoryDetailView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]

        return [IsAdmin()]
    def get_object(self,pk):
        try:
            return Category.objects.get(pk=pk)  
        except Category.DoesNotExist:
            return None

    def get(self, request, pk):

        category = self.get_object(pk)

        if category is None:
            return Response(
                {"message": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer =CategorySerializer(category)

        return Response(serializer.data)
    @extend_schema(
    request=CategorySerializer,
    responses=CategorySerializer
)
    def put(self, request, pk):

        category = self.get_object(pk)

        if category is None:
            return Response(
                {"message": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CategorySerializer(
            category,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @extend_schema(
    request=CategorySerializer,
    responses=CategorySerializer
)
    def patch(self, request, pk):

        category = self.get_object(pk)

        if category is None:
            return Response(
                {"message": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):

        category = self.get_object(pk)

        if category is None:
            return Response(
                {"message": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        category.delete()

        return Response(
            {"message": "Category deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


class MenuListCreateView(APIView):

    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):

        if self.request.method == 'GET':
            return [AllowAny()]

        return [IsAdmin()]

    def get(self, request):

        menu_items = MenuItem.objects.all()

        serializer = MenuItemSerializer(
            menu_items,
            many=True
        )

        return Response(serializer.data)

    @extend_schema(
        request=MenuItemSerializer,
        responses=MenuItemSerializer
    )
    def post(self, request):

        serializer = MenuItemSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
class MenuDetailView(APIView):

    def get_permissions(self):

        if self.request.method == 'GET':
            return [AllowAny()]

        return [IsAdmin()]

    def get_object(self, pk):

        try:
            return MenuItem.objects.get(pk=pk)

        except MenuItem.DoesNotExist:
            return None

    def get(self, request, pk):

        menu_item = self.get_object(pk)

        if menu_item is None:
            return Response(
                {"message": "Menu item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MenuItemSerializer(menu_item)

        return Response(serializer.data)

    def put(self, request, pk):

        menu_item = self.get_object(pk)

        if menu_item is None:
            return Response(
                {"message": "Menu item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MenuItemSerializer(
            menu_item,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):

        menu_item = self.get_object(pk)

        if menu_item is None:
            return Response(
                {"message": "Menu item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MenuItemSerializer(
            menu_item,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):

        menu_item = self.get_object(pk)

        if menu_item is None:
            return Response(
                {"message": "Menu item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        menu_item.delete()

        return Response(
            {"message": "Menu item deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
class CustomizationListCreateView(APIView):

    def get_permissions(self):

        if self.request.method == 'GET':
            return [AllowAny()]

        return [IsAdmin()]

    def get(self, request, menu_item_id):

        customizations = MenuItemCustomization.objects.filter(
            menu_item_id=menu_item_id
        )

        serializer = MenuItemCustomizationSerializer(
            customizations,
            many=True
        )

        return Response(serializer.data)

    def post(self, request, menu_item_id):

        data = request.data.copy()

        data["menu_item"] = menu_item_id

        serializer = MenuItemCustomizationSerializer(
            data=data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class CustomizationDetailView(APIView):
    

    def get_permissions(self):

        if self.request.method == 'GET':
            return [AllowAny()]

        return [IsAdmin()]

   
    def get_object(self, pk):

        try:
            return MenuItemCustomization.objects.get(pk=pk)

        except MenuItemCustomization.DoesNotExist:
            return None

    def get(self, request, pk):

        customization = self.get_object(pk)

        if customization is None:
            return Response(
                {"message": "Customization not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MenuItemCustomizationSerializer(
            customization
        )

        return Response(serializer.data)
    @extend_schema(
            request=MenuItemCustomizationSerializer,
            responses=MenuItemCustomizationSerializer)

    def put(self, request, pk):

        customization = self.get_object(pk)

        if customization is None:
            return Response(
                {"message": "Customization not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MenuItemCustomizationSerializer(
            customization,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):

        customization = self.get_object(pk)

        if customization is None:
            return Response(
                {"message": "Customization not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MenuItemCustomizationSerializer(
            customization,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):

        customization = self.get_object(pk)

        if customization is None:
            return Response(
                {"message": "Customization not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        customization.delete()

        return Response(
            {"message": "Customization deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )    






# Create your views here.
