from django.db.models import Q
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from account.serializers import UserSerializer
from post.models import Post
from post.serializers import PostSerializer
from journey.models import Journey
from journey.serializers import JourneySerializer


@api_view(['POST'])
def search(request):
    data = request.data
    query = data['query']
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    users = User.objects.filter(name__icontains=query)
    users_serializer = UserSerializer(users, many=True)

    posts = Post.objects.filter(
        Q(body__icontains=query, is_private=False) | 
        Q(created_by_id__in=list(user_ids), body__icontains=query)
    )

    journeys = Journey.objects.filter(
        Q(title__icontains=query, is_private=False, only_me=False) |
        Q(description__icontains=query, is_private=False, only_me=False) |
        Q(topic__icontains=query, is_private=False, only_me=False) |
        Q(title__icontains=query, created_by_id__in=list(user_ids), only_me=False) |
        Q(description__icontains=query, created_by_id__in=list(user_ids), only_me=False) |
        Q(topic__icontains=query, created_by_id__in=list(user_ids), only_me=False)
    )

    posts_serializer = PostSerializer(posts, many=True)
    journeys_serializer = JourneySerializer(journeys, many=True)

    return JsonResponse({
        'users': users_serializer.data,
        'posts': posts_serializer.data,
        'journeys': journeys_serializer.data
    }, safe=False)