from rest_framework import serializers

from account.serializers import UserSerializer
from journey.serializers import JourneySerializer

from .models import Conversation, ConversationMessage


class ConversationSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True, many=True)
    journey = JourneySerializer(read_only=True)

    class Meta:
        model = Conversation
        fields = ('id', 'users', 'modified_at_formatted', 'unread_messages', 'journey',)


class ConversationMessageSerializer(serializers.ModelSerializer):
    sent_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = ConversationMessage
        fields = ('id', 'sent_to', 'created_by', 'created_at_formatted', 'body', 'read')


class ConversationDetailSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True, many=True)
    messages = ConversationMessageSerializer(read_only=True, many=True)
    journey = JourneySerializer(read_only=True)

    class Meta:
        model = Conversation
        fields = ('id', 'users', 'modified_at_formatted', 'messages', 'journey', 'unread_messages')

