from django.http import JsonResponse
from django.views.decorators.http import require_POST

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from journey.models import Journey

from .models import Conversation, ConversationMessage
from .serializers import ConversationSerializer, ConversationDetailSerializer, ConversationMessageSerializer


@api_view(['GET'])
def conversation_list(request):
    conversations = Conversation.objects.filter(users__in=list([request.user]))
    conversations.order_by('-created_at')

    for conversation in conversations:
        messages = ConversationMessage.objects.filter(conversation=conversation)
        for message in messages:
            if not message.read and message.sent_to == request.user:
                conversation.unread_messages = True
                conversation.save()
                exit

    serializer = ConversationSerializer(conversations, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def conversation_detail(request, pk):
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    serializer = ConversationDetailSerializer(conversation)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def conversation_get_or_create(request, user_pk):
    user = User.objects.get(pk=user_pk)

    conversations = Conversation.objects.filter(journey=None).filter(users__in=list([request.user])).filter(users__in=list([user]))

    if conversations.exists():
        conversation = conversations.first()
    else:
        conversation = Conversation.objects.create()
        conversation.users.add(user, request.user)
        conversation.save()

    serializer = ConversationDetailSerializer(conversation)
    
    return JsonResponse(serializer.data, safe=False)

#Create journey groupchat
@api_view(['GET'])
def journey_conversation_create(request, journey_pk):
    journey = Journey.objects.get(pk=journey_pk)
    companions = journey.companions.all()

    if len(companions):
        conversation = Conversation.objects.create()
        conversation.users.add(request.user)
        conversation.journey = journey
        for user in companions:
            conversation.users.add(user)
        conversation.save()

        journey.groupchat = True
        journey.save()

    serializer = ConversationDetailSerializer(conversation)
    
    return JsonResponse(serializer.data, safe=False)

#Add new companion to groupchat
@api_view(['POST'])
def journey_conversation_add(request, journey_pk):
    journey = Journey.objects.filter(groupchat=True).get(pk=journey_pk)
    if journey:
        conversation = Conversation.objects.get(journey=journey)
        conversation.users.add(request.user)

        conversation.save()

        serializer = ConversationDetailSerializer(conversation)
        
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'message': 'There is no groupchat for this journey yet'})

@api_view(['POST'])
def conversation_send_message(request, pk):
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)

    for user in conversation.users.all():
        if user != request.user:
            sent_to = user

    conversation_message = ConversationMessage.objects.create(
        conversation=conversation,
        body=request.data.get('body'),
        created_by=request.user,
        sent_to=sent_to,
        read = False
    )

    serializer = ConversationMessageSerializer(conversation_message)

    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def readMessage(request, pk):
    message = ConversationMessage.objects.filter(sent_to=request.user).get(pk=pk)
    message.read = True
    message.save()

    conversation = message.conversation
    conversation.unread_messages = False
    conversation.save()

    return JsonResponse({'message' : 'Read message'})

@api_view(['GET'])
def checkMessages(request):

    unread_messages = ConversationMessage.objects.filter(sent_to=request.user, read=False)
    
    return JsonResponse(len(unread_messages), safe=False)

@require_POST
def createRoom(request, uuid):
    return JsonResponse({'message': 'room created'})