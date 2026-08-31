from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import  IsAuthenticated, IsAdminUser,AllowAny
from .permissions import IsAdmin
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
#from rest_framework.authentication import TokenAuthentication




#from django.contrib.auth.models import User
from .serializers import( 
    RegisterSerializer,
    LoginSerializer,
    ProfileSerializer,
    UserListSerializer,
    
)

class RegisterView(APIView):
   permission_classes=[AllowAny]
   @extend_schema(
        request=RegisterSerializer,
        responses={201: dict}
   )

   def post(self,request):
      serializer=RegisterSerializer(data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response({"message":"user register successfully"},status=status.HTTP_201_CREATED)
      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
   permission_classes=[AllowAny]
   @extend_schema(
        request=LoginSerializer,
        responses={200: dict}
    )
   def post(self,request):
      serializer=LoginSerializer(data=request.data)
      if serializer.is_valid():
          user = serializer.validated_data['user']

          refresh = RefreshToken.for_user(user) 

          return Response({
                "message": "Login successful",
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })

      return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
class ProfileView(APIView):

    permission_classes = [IsAuthenticated]
    @extend_schema(
        responses=ProfileSerializer
    )

    def get(self, request):

        serializer = ProfileSerializer(
            request.user
        )

        return Response(
            serializer.data
        )
    @extend_schema(
        request=ProfileSerializer,
        responses=ProfileSerializer
    )

    def put(self, request):

        serializer = ProfileSerializer(
            request.user,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
class AdminUsersView(APIView):

    permission_classes = [IsAdmin]
    @extend_schema(
        responses=UserListSerializer(many=True)
    )

    def get(self, request):

        users = User.objects.all()

        serializer = UserListSerializer(
           users,
            many=True
        )

        return Response(
            serializer.data
        )    


   
    



# Create your views here.
