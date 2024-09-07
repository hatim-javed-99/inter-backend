from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import SignupViewSet, LoginViewSet, UserSearchView, CreateSuperUserAPIView

router = DefaultRouter()
router.register("signup", SignupViewSet, basename="signup")
router.register("login", LoginViewSet, basename="login")
router.register("search", UserSearchView, basename="search")

urlpatterns = [
    path("", include(router.urls)),
    path('forgot-password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('create-superuser/', CreateSuperUserAPIView.as_view(), name='create-superuser'),
]