import uuid

from django.db import models

from account.models import User
from post.models import Post
from journey.models import Journey


class Notification(models.Model):
    NEWFRIENDREQUEST = 'new_friendrequest'
    ACCEPTEDFRIENDREQUEST = 'accepted_friendrequest'
    REJECTEDFRIENDREQUEST = 'rejected_friendrequest'
    POST_LIKE = 'post_like'
    POST_COMMENT = 'post_comment'
    COMPANION_REQUEST = 'companion_request'
    ACCEPTEDCOMPANIONREQUEST = 'accepted_companionrequest'
    REJECTEDCOMPANIONREQUEST = 'rejected_companionrequest'
    FOLLOWEDJOURNEY = 'journey_follow'

    CHOICES_TYPE_OF_NOTIFICATION = (
        (NEWFRIENDREQUEST, 'New friendrequest'),
        (ACCEPTEDFRIENDREQUEST, 'Accepted friendrequest'),
        (REJECTEDFRIENDREQUEST, 'Rejected friendrequest'),
        (POST_LIKE, 'Post like'),
        (POST_COMMENT, 'Post comment'),
        (COMPANION_REQUEST, 'Companion request'),
        (ACCEPTEDCOMPANIONREQUEST, 'Accepted companionrequest'),
        (REJECTEDCOMPANIONREQUEST, 'Rejected companionrequest'),
        (FOLLOWEDJOURNEY, 'Followed journey')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    type_of_notification = models.CharField(max_length=50, choices=CHOICES_TYPE_OF_NOTIFICATION)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='created_notifications', on_delete=models.CASCADE)
    created_for = models.ForeignKey(User, related_name='received_notifications', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)