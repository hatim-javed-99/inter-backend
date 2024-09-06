from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from users.api.v1.serializer import SignupSerializer, UserSerializer, LoginSerializer
from users.models import Profile


class SignupViewSet(ModelViewSet):
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["post"]


class LoginViewSet(ViewSet):
    """Based on rest_framework.authtoken.views.ObtainAuthToken"""

    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        profile = Profile.objects.filter(user=user).first()
        user_serializer = UserSerializer(profile, context={"request": request})
        return Response({"token": token.key, "user": user_serializer.data})


class UserSearchView(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["get"]

    def get_queryset(self):
        name = self.request.query_params.get("name")
        if name:
            queryset = Profile.objects.filter(name__icontains=name)
        else:
            queryset = Profile.objects.all()
        return queryset