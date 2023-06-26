from authentication.serializers import PostSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view
from authentication.models import Post

@api_view(['POST'])
def create_post(request):
    serializer = PostSerializer(data=request.data)

    if serializer.is_valid():
        post = serializer.save(user=request.user)
        return JsonResponse({'id': post.id, 'message': 'Post created successfully'})
    else:
        return JsonResponse(serializer.errors, status=400)
    
@api_view(['GET'])
@login_required
def get_user_data(request):
    user = request.user

    # Retrieve user data
    data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        # Add any additional fields you want to include
    }

    return JsonResponse(data)

@api_view(['POST'])
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.likes.add(request.user)
    post.save()
    return JsonResponse({'message': 'Post liked successfully'})

@api_view(['POST'])
def unlike_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.likes.remove(request.user)
    post.save()
    return JsonResponse({'message': 'Post unliked successfully'})
