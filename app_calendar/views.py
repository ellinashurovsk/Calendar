from django.shortcuts import render
from .models import Meeting
from .serializers import MeetingSerializer
import json
from urllib import request

from django.http import JsonResponse
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes


@authentication_classes([])
@permission_classes([])
class NewUser(GenericAPIView):
    """
    Create a new user.

    """

    def post(self, request):
        post_body = json.loads(request.body)

        in_username = post_body.get('username')
        in_password = post_body.get('password')

        extra_user_data = {}
        if 'first_name' in post_body:
            in_first_name = post_body.get('first_name')
            extra_user_data['first_name'] = in_first_name

        if 'last_name' in post_body:
            in_last_name = post_body.get('last_name')
            extra_user_data['last_name'] = in_last_name

        if 'email' in post_body:
            in_email = post_body.get('email')
            extra_user_data['email'] = in_email

        try:
            user = User.objects.get(username=in_username)

            data = {
                'success': False,
                'details': 'Username already exists.'
            }
            return Response(data)

        except User.DoesNotExist:

            user = User.objects.create_user(
                username=in_username, password=in_password, **extra_user_data)

            data = {
                'success': True,
                'payload': {
                    'id': user.id,
                    'username': user.username
                }
            }
            return JsonResponse(data, status=201)


class SingleMeeting(GenericAPIView):
    """
    Get meeting details.

    * Requires token authentication.

    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):

        in_owner_id = request.user.id  # get meeting details for the current user

        try:
            meeting = Meeting.objects.get(
                pk=kwargs['in_pk'], owner_id=in_owner_id)
            meeting_serial = MeetingSerializer(meeting)

            data = {
                'success': True,
                'payload': {
                    'id': meeting_serial.data['id'],
                    'owner_id': meeting_serial.data['owner'],
                    'name': meeting_serial.data['meeting_name'],
                    'date': meeting_serial.data['date'],
                }
            }
            return Response(data)

        except Meeting.DoesNotExist:
            data = {
                'success': False,
            }
            return JsonResponse(data)


class Meetings(GenericAPIView):
    """
    POST:
          Create a new meeting.

    GET:
          Get meetings according the information provided.

    |---------------|-----------------------------------------------------|-----------------------------------------------------------------------------|
    | INFO PROVIDED |   DESCRIPTION                                       |  QUERY STRING EXAMPLE                                                       |
    |---------------|-----------------------------------------------------|-----------------------------------------------------------------------------|
    |       -       | - Return all the meetings for the current user      |  http://127.0.0.1:8000/meetings                                             |
    |---------------|-----------------------------------------------------|-----------------------------------------------------------------------------|
    |  start_date   | - Return meetings for the current user              |  http://127.0.0.1:8000/meetings?start_date=2022-05-28                       |
    |               | from the start date.                                |                                                                             |
    |---------------|-----------------------------------------------------|-----------------------------------------------------------------------------|
    |  end_date     | - Return meetings for the current user              |  http://127.0.0.1:8000/meetings?end_date=2022-06-26                         |
    |               | untill the end date.                                |                                                                             |
    |---------------|-----------------------------------------------------|-----------------------------------------------------------------------------|
    |  start_date,  | - Return meetings for the current user              |  http://127.0.0.1:8000/meetings?start_date=2022-05-28&end_date=2022-06-26   |
    |  end_date     | for the period of time.                             |                                                                             |
    |---------------|-----------------------------------------------------|-----------------------------------------------------------------------------|

    * Requires token authentication.

    """

    permission_classes = (IsAuthenticated,)
    serializer_class = MeetingSerializer

    def post(self, request):
        post_body = json.loads(request.body)

        in_owner_id = request.user.id  # create a new meeting for the current user
        in_name = post_body.get('name')
        in_date = post_body.get('date')
        in_participants = post_body.get('participants')

        users = User.objects.filter(username=in_participants)
        instance = Meeting.objects.create(
            owner_id=in_owner_id, meeting_name=in_name, date=in_date)

        instance.participants.set(users)

        data = {
            'success': True,
            'payload': {
                'id': instance.id,
                'owner_id': instance.owner_id,
                'name': instance.meeting_name.title(),
                'date': instance.date
            }
        }
        return JsonResponse(data, status=201)

    def get(self, request):

        in_owner_id = request.user.id  # get meetings for the current user
        in_data = {}

        if 'start_date' in request.GET:
            in_data['date__gte'] = request.GET['start_date']

        if 'end_date' in request.GET:
            in_data['date__lte'] = request.GET['end_date']

        meetings = Meeting.objects.filter(owner_id=in_owner_id)
        meetings = meetings.filter(**in_data)

        meetings_serial = MeetingSerializer(meetings, many=True)

        data = {}
        if meetings_serial.data:
            data['success'] = True
            data['payload'] = []
            for i in range(len(meetings_serial.data)):
                dct = {}
                dct['id'] = meetings_serial.data[i]['id']
                dct['owner_id'] = meetings_serial.data[i]['owner']
                dct['name'] = meetings_serial.data[i]['meeting_name']
                dct['date'] = meetings_serial.data[i]['date']
                data['payload'].append(dct)
        else:
            data = {
                'success': False,
            }

        return JsonResponse(data)
