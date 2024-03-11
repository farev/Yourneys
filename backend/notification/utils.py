from .models import Notification
from .consumers import NotificationConsumer

from post.models import Post
from account.models import FriendshipRequest
from journey.models import Journey

from channels.layers import get_channel_layer 
from asgiref.sync import async_to_sync
import json


# create_notification(request, 'post_like', 'lskjf-j12l3-jlas-jdfa', 'lskjf-j12l3-jlas-jdfa')


def create_notification(request, type_of_notification, post_id=None, journey_id=None, friendrequest_id=None):
    created_for = None

    if type_of_notification == 'post_like':
        body = f'{request.user.name} liked one of your posts!'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by

    elif type_of_notification == 'post_comment':
        body = f'{request.user.name} commented on one of your posts!'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by

    elif type_of_notification == 'new_friendrequest':
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for
        body = f'{request.user.name} sent you a friend request!'

    elif type_of_notification == 'accepted_friendrequest':
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for
        body = f'{request.user.name} accepted your friend request!'

    elif type_of_notification == 'rejected_friendrequest':
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for
        body = f'{request.user.name} rejected your friend request!'

    elif type_of_notification == 'accepted_companionrequest':
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_by
        body = f'{request.user.name} accecpted your companion request!'

    elif type_of_notification == 'rejected_companionreques':
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_by
        body = f'{request.user.name} rejected your companion request!'

    elif type_of_notification == 'journey_follow':
        journey = Journey.objects.get(pk=journey_id)
        created_for = journey.created_by
        body = f'{request.user.name} started following {journey.title}!'


    notification = Notification.objects.create(
        body=body,
        type_of_notification=type_of_notification,
        created_by=request.user,
        post_id=post_id,
        journey_id=journey_id,
        created_for=created_for
    )

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'notifications', {
            'type': 'send_notification',
            'message': 'Send notification'
        }
    )

    print(channel_layer)

    return notification