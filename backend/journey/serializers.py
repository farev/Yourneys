from rest_framework import serializers

from account.serializers import UserSerializer
from post.serializers import PostSerializer

from .models import Journey

class JourneySerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    posts = PostSerializer(read_only=True, many=True)

    class Meta:
        model = Journey 
        fields = ('id', 'title', 'description', 'topic', 'is_private', 'on_going', 'posts', 'created_by', 'created_at_formatted')

class JourneyDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Journey 
        fields = ('id', 'title', 'description', 'topic', 'is_private', 'on_going', 'created_by', 'created_at_formatted')
