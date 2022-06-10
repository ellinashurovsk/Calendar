from django.db import models
from django.contrib.auth.models import User


class Meeting(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    meeting_name = models.CharField(max_length=200)
    date = models.DateTimeField()
    date_added = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User, related_name='participants')

    def __str__(self):
        """Return a string representation of the model."""
        return self.meeting_name
