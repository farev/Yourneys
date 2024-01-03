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

#Create new journey
@api_view(['POST'])
def journey_create(request):
    form = JourneyForm(request.POST)

    if form.is_valid():
        journey = form.save(commit=False)
        journey.created_by = request.user
        journey.save()

        user = request.user
        #user.posts_count = user.posts_count + 1
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

    if not request.user in user.friends.all():
        journeys = journeys.filter(is_private=False)

    journeys_serializer = JourneySerializer(journeys, many=True)
    user_serializer = UserSerializer(user)

    can_send_friendship_request = True

    if request.user in user.friends.all():
        can_send_friendship_request = False
    
    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

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
    return JsonResponse({
        'journey': JourneySerializer(journey).data
    })

#Get list of journeys for feed
@api_view(['GET'])
def journey_feed_list(request):
    journeys = Journey.objects.filter(~Q(posts = None))
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
