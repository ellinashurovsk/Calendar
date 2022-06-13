from rest_framework.serializers import ModelSerializer
from .models import Meeting


class MeetingSerializer(ModelSerializer):

    class Meta:
        model = Meeting
        fields = "__all__"
