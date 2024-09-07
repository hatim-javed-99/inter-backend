from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.utils import email_address_exists, generate_unique_username
from django.contrib.auth import get_user_model, authenticate
from django.db import transaction
from django.http import HttpRequest
from rest_framework import serializers, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from users.models import Profile

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=False, allow_null=True)
    address = serializers.CharField(max_length=600, required=False, allow_null=True)
    profile_image = serializers.FileField(required=False, allow_null=True)
    dob = serializers.DateField(required=False, allow_null=True)
    name = serializers.CharField(max_length=100, required=False, allow_null=True)
    gender = serializers.CharField(max_length=6, required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'password', 'phone', 'name', 'gender', 'profile_image', 'dob', 'address')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            },
        }

    def _get_request(self):
        request = self.context.get('request')
        if request and not isinstance(request, HttpRequest) and hasattr(request, '_request'):
            request = request._request
        return request

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError("A user is already registered with this e-mail address.")
        return email

    @transaction.atomic
    def create(self, validated_data):
        try:
            # Create the user instance
            user = User(
                email=validated_data.get('email'),
                username=generate_unique_username([
                    validated_data.get('email'),
                    'user'
                ])
            )
            user.set_password(validated_data.get('password'))
            user.save()

            # Prepare profile data
            serializer_data = {
                "address": validated_data.get('address'),
                "profile_image": validated_data.get('profile_image'),
                "dob": validated_data.get('dob'),
                "phone": validated_data.get('phone'),
                "gender": validated_data.get('gender'),
                "name": validated_data.get('name'),
            }

            # Fetch the user's profile
            user_profile = Profile.objects.get(user_id=user.id)

            # Update the profile using serializer
            serializer = UserSerializer(instance=user_profile, data=serializer_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return serializer.data

        except ValidationError as e:
            # Rollback the transaction if validation fails
            transaction.set_rollback(True)
            raise e

        except Exception as e:
            # Handle other exceptions
            transaction.set_rollback(True)
            return serializers.ValidationError({"error": str(e)})


class LoginSerializer(AuthTokenSerializer):

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        username = User.objects.filter(email=username).first()

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username.username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = ('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            if not user.is_active:
                raise AuthenticationFailed("Unable to log in. Your account is deactivated.")
        else:
            msg = ('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"
        extra_kwargs = {"user": {"required": False}}


class ProfileUpdateSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"
        extra_kwargs = {"user": {"required": False}}


#

class AbstractUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "is_active"]


class SuperUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_superuser(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user