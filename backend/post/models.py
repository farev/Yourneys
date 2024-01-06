import uuid

from django.conf import settings
from django.db import models
from django.utils.timesince import timesince
from django.core.validators import FileExtensionValidator 

from account.models import User

class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)
    
    def created_at_formatted(self):
       return timesince(self.created_at)


class PostAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #image = models.ImageField(upload_to='post_attachments')
    file = models.FileField(upload_to='post_attachments', blank=True, null=True)
    #video = models.FileField(upload_to='videos_uploaded',null=True, validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])    
    created_by = models.ForeignKey(User, related_name='post_attachments', on_delete=models.CASCADE)

    def get_file(self):
        if self.file:
            return settings.WEBSITE_URL + self.file.url
        else:
            return ''


class Post(models.Model):
    post_label_choices = [
        ('Start', 'Start'),
        ('Update', 'Update'),
        ('Milestone', 'Milestone'),
        ('End', 'End') 
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)

    journeyid = models.TextField(blank=True, null=True)
    label = models.CharField(max_length=10, choices=post_label_choices, default='Update',)

    attachments = models.ManyToManyField(PostAttachment, blank=True)

    is_private = models.BooleanField(default=False)

    likes = models.ManyToManyField(Like, blank=True)
    likes_count = models.IntegerField(default=0)

    comments = models.ManyToManyField(Comment, blank=True)
    comments_count = models.IntegerField(default=0)

    reported_by_users = models.ManyToManyField(User, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)
    
    def created_at_formatted(self):
       return timesince(self.created_at)
    

class Trend(models.Model):
    hashtag = models.CharField(max_length=255)
    occurences = models.IntegerField()