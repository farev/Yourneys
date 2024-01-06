from django.db.models import Q
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User, FriendshipRequest
from account.serializers import UserSerializer
from notification.utils import create_notification

from .forms import PostForm, AttachmentForm
from .models import Post, Like, Comment, Trend, PostAttachment
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, TrendSerializer

from journey.models import Journey
from journey.serializers import JourneySerializer
from journey.api import save_Journey


@api_view(['GET'])
def post_list(request):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    posts = Post.objects.filter(created_by_id__in=list(user_ids))

    trend = request.GET.get('trend', '')

    if trend:
        posts = posts.filter(body__icontains='#' + trend).filter(is_private=False)

    serializer = PostSerializer(posts, many=True)

    return JsonResponse(serializer.data, safe=False)

#Gets the information for post view
@api_view(['GET'])
def post_detail(request, pk): 
    user_ids = [request.user.id]

    post = Post.objects.filter(Q(created_by_id__in=list(user_ids)) | Q(is_private=False)).get(pk=pk)
    journey = Journey.objects.get(id=post.journeyid)    

    for user in request.user.friends.all():
        user_ids.append(user.id)


    return JsonResponse({
        'post': PostDetailSerializer(post).data,
        'journey': JourneySerializer(journey).data
    })

#Get list of posts from a user in the profile
@api_view(['GET'])
def post_list_profile(request, id):   
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)

    if not request.user in user.friends.all():
        posts = posts.filter(is_private=False)

    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    can_send_friendship_request = True

    if request.user in user.friends.all():
        can_send_friendship_request = False
    
    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if check1 or check2:
        can_send_friendship_request = False

    return JsonResponse({
        'posts': posts_serializer.data,
        'user': user_serializer.data,
        'can_send_friendship_request': can_send_friendship_request
    }, safe=False)

#Create post
@api_view(['POST'])
def post_create(request):
    form = PostForm(request.POST)
    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)
    #attachments = PostAttachment.objects.none()
    #journeys = Journey.objects.filter(created_by_id=request.user.id)
    #journey = Journey.objects.get(id = post.journeyID)


    if attachment_form.is_valid():
        #attachments = attachment_form.files
        #attachments = request.FILES.getlist()
        #for attachment in attachments: 
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        if attachment:
            post.attachments.add(attachment)
            
        journey = Journey.objects.get(id=post.journeyid)
        journey.posts.add(post)
        journey.save()

        #save_Journey(post.journeyID)

        #for attachment in attachments:
            #post.attachments.add(attachment)

        user = request.user
        user.posts_count = user.posts_count + 1
        user.save()

        serializer = PostSerializer(post)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add somehting here later!...'})
    
#Edit post
@api_view(['POST'])
def post_edit(request, pk):
    form = PostForm(request.POST)
    post = Post.objects.filter(created_by=request.user).get(pk=pk)
    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)

    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    if form.is_valid():
        form.save(commit=False)
        post.created_by = request.user
        post.body = form.data['body']
        post.is_private = form['is_private'].value()
        post.label = form.data['label']
        post.save()

        if attachment:
            post.attachments.add(attachment)
            
        journey = Journey.objects.get(id=post.journeyid)
        #journey.posts.add(post)
        journey.posts.update(post)
        journey.save()

        serializer = PostSerializer(post)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add somehting here later!...'})
    
#Like post
@api_view(['POST'])
def post_like(request, pk):
    post = Post.objects.get(pk=pk)

    if not post.likes.filter(created_by=request.user):
        like = Like.objects.create(created_by=request.user)

        post = Post.objects.get(pk=pk)
        post.likes_count = post.likes_count + 1
        post.likes.add(like)
        post.save()

        notification = create_notification(request, 'post_like', post_id=post.id)

        return JsonResponse({'message': 'like created'})
    else:
        return JsonResponse({'message': 'post already liked'})

#Comment on post
@api_view(['POST'])
def post_create_comment(request, pk):
    comment = Comment.objects.create(body=request.data.get('body'), created_by=request.user)

    post = Post.objects.get(pk=pk)
    post.comments.add(comment)
    post.comments_count = post.comments_count + 1
    post.save()

    notification = create_notification(request, 'post_comment', post_id=post.id)

    serializer = CommentSerializer(comment)

    return JsonResponse(serializer.data, safe=False)

#Delete post
@api_view(['DELETE'])
def post_delete(request, pk):
    post = Post.objects.filter(created_by=request.user).get(pk=pk)
    post.delete()

    return JsonResponse({'message': 'post deleted'})

#Report post
@api_view(['POST'])
def post_report(request, pk):
    post = Post.objects.get(pk=pk)
    post.reported_by_users.add(request.user)
    post.save()

    return JsonResponse({'message': 'post reported'})

#Get trends
@api_view(['GET'])
def get_trends(request):
    serializer = TrendSerializer(Trend.objects.all(), many=True)

    return JsonResponse(serializer.data, safe=False)