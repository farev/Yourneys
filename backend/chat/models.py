import uuid

from django.db import models
from django.utils.timesince import timesince

from account.models import User
from journey.models import Journey


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    unread_messages = models.BooleanField(default=False)
    journey = models.OneToOneField(Journey, on_delete=models.CASCADE, null=True)
    
    def modified_at_formatted(self):
       return timesince(self.created_at)


class ConversationMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    body = models.TextField()
    sent_to = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    
    def created_at_formatted(self):
       return timesince(self.created_at)