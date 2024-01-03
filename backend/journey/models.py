from django.db import models
import uuid
from django.conf import settings
from django.utils.timesince import timesince

from account.models import User
from post.models import Post

class Journey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    topic = models.TextField(blank=True, null=True)
    is_private = models.BooleanField(default=False)
    on_going = models.BooleanField(default=True)

    posts = models.ManyToManyField(Post, blank=True, editable=True)

    reported_by_users = models.ManyToManyField(User, blank=True, related_name='Journey')

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='journey', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)
    
    def created_at_formatted(self):
       return timesince(self.created_at)
    