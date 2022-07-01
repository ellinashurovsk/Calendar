from .models import Meeting
from .serializers import MeetingSerializer
from .permissions import IsOwnerOrReadOnly

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


start_date = openapi.Parameter(
    name='start_date', description='Start date of the date range', in_=openapi.IN_QUERY, type=openapi.FORMAT_DATE)
end_date = openapi.Parameter(
    name='end_date', description='End date of the date range', in_=openapi.IN_QUERY, type=openapi.FORMAT_DATE)


class MeetingsViewSet(viewsets.ModelViewSet):

    model = Meeting
    serializer_class = MeetingSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Optionally restricts the returned meetings to the currently authenticated user,
        by filtering against a 'start_date' and 'end_date' query parameter in the URL.
        """
        queryset = Meeting.objects.filter(owner=self.request.user)

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            queryset = queryset.filter(date__gte=start_date)

        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        return queryset

    def create(self, request):
        # Create a new post for the currently authenticated user.

        serializer = MeetingSerializer(data=request.data)
        serializer.is_valid()
        serializer.save(owner=request.user)

        return Response(serializer.data, status=201)

    @swagger_auto_schema(operation_description="Return a list of the meetings for the currently authenticated user. Optionally restricts the returned meetings, by filtering against a 'start_date' and 'end_date' query parameter in the URL.", manual_parameters=[start_date, end_date],)
    def list(self, request, *args, **kwargs):
        # Return a list of the meetings for the currently authenticated user.

        queryset = self.get_queryset()
        serializer = MeetingSerializer(queryset, many=True)
        return Response(serializer.data)
