from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    UserSerializer,
    UserListSerializer,
    TokenObtainPairResponseSerializer,
    TokenRefreshResponseSerializer
)

from rest_framework.permissions import (
    IsAdminUser,
    AllowAny,
    IsAuthenticated
)
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


class UsersAPIList(ListAPIView):
    """
    View to return all existing users.

    * Requires JWT token authentication.
    * Only admin user is able to access this view.
    """

    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]


class UserAPICreate(CreateAPIView):
    """
    View to create a new user.

    * Doesn't require JWT token authentication.
    * Everyone is able to access this view.
    """

    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = [AllowAny]


class UserAPIReadUpdateDelete(RetrieveUpdateDestroyAPIView):
    """
    GET: Return a user by it's id.

    PUT: Update a user by it's id.

    PATCH: Update a user by it's id.

    DELETE: Delete a user by it's id.

    * Requires JWT token authentication.
    * GET - method is allowed for authenticated users,
      PUT, PATCH, DELETE  - methods are allowed only for the users themselves

    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "id"


###########################Authorization########################################


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
