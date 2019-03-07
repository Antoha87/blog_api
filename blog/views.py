from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, views
from .serializers import PostSerializer
from django.contrib.auth.models import User
from .models import Post, Like
from django.http import JsonResponse


class PostViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing post instances.
    """
    serializer_class = PostSerializer
    queryset = Post.objects.prefetch_related('author', 'likes')
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'


class LikeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, slug):
        obj = get_object_or_404(Post, slug=slug)
        user = User.objects.get(id=request.user.id)
        try:
            like = Like.objects.get(user=user, post=obj)
            like.delete()
            return JsonResponse({'message': 'delete like'})
        except Like.DoesNotExist:
            Like.objects.create(user=user, post=obj)
            return JsonResponse({'message': 'add like'})


