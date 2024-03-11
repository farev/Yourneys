from rest_framework import serializers

from .models import User, FriendshipRequest

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'friends_count', 'journeys_count', 'posts_count', 'get_avatar',)

class UserSerializer(serializers.ModelSerializer):
    friends = FriendSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'friends', 'friends_count', 'journeys_count', 'posts_count', 'get_avatar',)


class FriendshipRequestSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_for = UserSerializer(read_only=True)
     
    class Meta:
        model = FriendshipRequest
        fields = ('id', 'created_by', 'created_for', 'journeyid')