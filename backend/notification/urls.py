from django.urls import path

from . import api


urlpatterns = [
    path('', api.notifications, name='notifications'),
    path('read/<uuid:pk>/', api.read_notification, name='read_notification'),
    path('check/', api.check_notifications, name='check_notifications'),
]