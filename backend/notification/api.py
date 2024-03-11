from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Notification
from .serializers import NotificationSerializer
from account.models import FriendshipRequest


@api_view(['GET'])
def notifications(request):
    received_notifications = request.user.received_notifications.filter(is_read=False)
    serializer = NotificationSerializer(received_notifications, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def read_notification(request, pk):
    notification = Notification.objects.filter(created_for=request.user).get(pk=pk)
    notification.is_read = True
    notification.save()

    return JsonResponse({'message': 'notification read'})
    return 

@api_view(['GET'])
def check_notifications(request):
    unread_notifications = Notification.objects.filter(created_for=request.user, is_read=False)
    unread_requests = FriendshipRequest.objects.filter(status='sent')
    number = len(unread_notifications) + len(unread_requests)
    return JsonResponse(number, safe=False)