from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['id','username','email','password','role','is_active','created_at']
       # extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
            user=User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                role=validated_data.get('role'),
                password=validated_data['password'],

            )
            return user
        # def  create(self,validated_data):
        #     password=validated_data.pop('password')
        #     user=User(**validated_data)
        #     user.set_password(password)
        #     user.save()

        #     return user


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):

        username=data.get('username')
        password=data.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            raise serializers.ValidationError(
                "Invalid username or password"
            )

        data['user'] = user

        return data
class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            'id',
            'username',
            'email',
            'role'
        ]

        read_only_fields = ['role']
class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            'id',
            'username',
            'email',
            'role',
            'is_active'
        ]        