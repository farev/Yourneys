from rest_framework import serializers

from account.serializers import UserSerializer
from post.serializers import PostSerializer

from .models import Journey 

class JourneySerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    companions = UserSerializer(read_only=True, many=True)
    posts = PostSerializer(read_only=True, many=True)

    class Meta:
        model = Journey 
        fields = ('id', 'title', 'description', 'topic', 'is_private', 'only_me', 'on_going', 'posts', 'created_by', 'created_at_formatted', 'companions', 'groupchat', 'followed_by_users', 'follower_count')

class JourneyDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    companions = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Journey 
        fields = ('id', 'title', 'description', 'topic', 'is_private', 'only_me', 'on_going', 'created_by', 'created_at_formatted', 'companions', 'followed_by_users', 'follower_count')
