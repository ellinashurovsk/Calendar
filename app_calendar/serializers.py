from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Meeting


class MeetingSerializer(ModelSerializer):

    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Meeting
        fields = "__all__"

# from rest_framework import serializers
# from .models import Meeting


# class MeetingSerializer(serializers.Serializer):

#     owner = serializers.IntegerField()
#     meeting_name = serializers.CharField(max_length=200)
#     date = serializers.DateTimeField()
#     date_added = serializers.DateTimeField()
#     participants = serializers.ListField(
#         child=serializers.IntegerField(min_value=0, max_value=100))
