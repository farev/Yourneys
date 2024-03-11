from django.http import JsonResponse
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User, FriendshipRequest
from account.serializers import UserSerializer
from .forms import JourneyForm
from .serializers import JourneySerializer
from .models import Journey
from post.serializers import PostSerializer
from post.models import Post
from notification.utils import create_notification


#Create new journey
@api_view(['POST'])
def journey_create(request):
    form = JourneyForm(request.POST)

    if form.is_valid():
        journey = form.save(commit=False)
        journey.created_by = request.user
        journey.save()

        user = request.user
        user.journeys_count = user.journeys_count + 1
        user.save()

        serializer = JourneySerializer(journey)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add somehting here later!...'})
    
#Get list of journeys to display in user profile
@api_view(['GET'])
def journey_list_profile(request, id):   
    user = User.objects.get(pk=id)
    journeys = Journey.objects.filter(created_by_id=id)
    can_send_friendship_request = False


    if user != request.user:
        journeys = journeys.filter(only_me=False)

        if not request.user in user.friends.all():
            journeys = journeys.filter(is_private=False)
            can_send_friendship_request = True
            print(can_send_friendship_request)


    journeys_serializer = JourneySerializer(journeys, many=True)
    user_serializer = UserSerializer(user)

    if request.user in user.friends.all():
        can_send_friendship_request = False
    
    check1 = FriendshipRequest.objects.filter(journeyid='').filter(created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(journeyid='').filter(created_for=user).filter(created_by=request.user)

    if check1 or check2:
        can_send_friendship_request = False

    return JsonResponse({
        'journeys': journeys_serializer.data,
        'user': user_serializer.data,
        'can_send_friendship_request': can_send_friendship_request,
        #'posts': post_list_profile(request).posts

    }, safe=False)

#Get data for journey view
@api_view(['GET']) 
def journey_view(request, pk):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    #post = Post.objects.filter(Q(created_by_id__in=list(user_ids)) | Q(is_private=False)).get(pk=pk)
    journey = Journey.objects.get(pk=pk)
    try:
        conversation = journey.conversation.id
    except: 
        conversation = '0'

    return JsonResponse({
        'journey': JourneySerializer(journey).data,
        'conversation': conversation
    })

#Get list of journeys for feed
@api_view(['GET'])
def journey_feed_list(request):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    journeys = Journey.objects.filter(~Q(posts = None)).filter(only_me=False, is_private=False) | Journey.objects.filter(~Q(posts = None), only_me=False, is_private=True, created_by_id__in=list(user_ids))
    user = request.user
    all_posts = Post.objects.none()

    for journey in journeys:
        postsInJourney = journey.posts.all()
        all_posts = all_posts | postsInJourney

    all_posts.order_by('-created_at')

    journeys_serializer = JourneySerializer(journeys, many=True)
    user_serializer = UserSerializer(user)
    post_serializer = PostSerializer(all_posts, many=True, read_only=True)

    return JsonResponse({
        'journeys': journeys_serializer.data,
        'user': user_serializer.data,
        'posts': post_serializer.data
    })

#Get list of journeys for following feed
@api_view(['GET'])
def journey_following_list(request):
    user = request.user
    journeys = []

    for journey in Journey.objects.all():
        for follower in journey.followed_by_users.all():
            if follower.id == user.id:
                #journeys = journeys | journey
                journeys.append(journey)
                

    #journeys = Journey.objects.filter(~Q(posts = None))

    #journeys.order_by('-created_at')

    journeys_serializer = JourneySerializer(journeys, many=True)
    user_serializer = UserSerializer(user)

    return JsonResponse({
        'journeys': journeys_serializer.data,
        'user': user_serializer.data,
    })

#Edit journey
@api_view(['POST'])
def journey_edit(request, pk):
    form = JourneyForm(request.POST)
    journey = Journey.objects.filter(created_by=request.user).get(pk=pk)

    if form.is_valid():
        form.save(commit=False)
        journey.title = form.data['title']
        journey.description = form.data['description']
        journey.topic = form.data['topic']
        journey.is_private = form['is_private'].value()
        journey.only_me = form['only_me'].value()
        journey.save()
        serializer = JourneySerializer(journey)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add somehting here later!...'})

#Delete journey
@api_view(['DELETE'])
def journey_delete(request, pk):
    journey = Journey.objects.filter(created_by=request.user).get(pk=pk)
    journey.delete()

    user = request.user
    user.journeys_count = user.journeys_count - 1
    user.save()

    return JsonResponse({'message': 'journey deleted'})

#Report journey
@api_view(['POST'])
def journey_report(request, pk):
    journey = Journey.objects.get(pk=pk)
    journey.reported_by_users.add(request.user)
    journey.save()

    return JsonResponse({'message': 'journey reported'})

def save_Journey(ID):
    journey = Journey.objects.get(id = ID)
    journey.save()

#Follow journey
@api_view(['POST'])
def journey_follow(request, pk):
    journey = Journey.objects.get(pk=pk)
    journey.followed_by_users.add(request.user)
    journey.follower_count = journey.follower_count + 1
    journey.save()

    notification = create_notification(request, 'journey_follow', journey_id=journey.id)
    
    return JsonResponse({'message': 'journey followed'})

#Unfollow journey
@api_view(['POST'])
def journey_unfollow(request, pk):
    journey = Journey.objects.get(pk=pk)
    journey.followed_by_users.remove(request.user)
    journey.follower_count = journey.follower_count - 1
    journey.save()

    return JsonResponse({'message': 'journey unfollowed'})


#Send companion request
@api_view(['POST'])
def send_companion_request(request, journeyID, pk):
    journey = Journey.objects.get(id=journeyID)
    user = User.objects.get(pk=pk)

    check1 = FriendshipRequest.objects.filter(journeyid=journey.id).filter(created_for=user).filter(created_by=request.user)
    #check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if not check1:
        friendrequest = FriendshipRequest.objects.create(created_for=user, created_by=request.user, journeyid=journey.id)

        #notification = create_notification(request, 'companion_request', friendrequest_id=friendrequest.id)

        return JsonResponse({'message': 'companion request created'})
    else:
        return JsonResponse({'message': 'request already sent'})

#Handle companion request
@api_view(['POST'])
def handle_request(request, journeyID, status):
    journey = Journey.objects.get(id=journeyID)
    companionRequest = FriendshipRequest.objects.filter(journeyid=journeyID).get(created_for=request.user)
    companionRequest.status = status
    companionRequest.save()

    if status == "accepted":
        print(companionRequest.created_for)
        journey.companions.add(companionRequest.created_for)
        journey.save()
        notification = create_notification(request, 'accepted_companionrequest', friendrequest_id=companionRequest.id, journey_id=journey.id)
        companionRequest.delete()
        

    elif status == "rejected":
        notification = create_notification(request, 'rejected_companionrequest', friendrequest_id=companionRequest.id, journey_id=journey.id)
        companionRequest.delete()


    return JsonResponse({'message': 'friendship request updated'})

#Remove Companion
@api_view(['POST'])
def remove_companion(request, journeyID, pk):
    journey = Journey.objects.filter(created_by=request.user).get(pk=journeyID)
    rem_User = User.objects.get(id=pk)
    journey.companions.remove(rem_User)
    journey.save()

    return JsonResponse({'message': 'companion removed'})