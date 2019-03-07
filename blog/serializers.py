from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Post, Like
from api.serializers import UserSerializer


class PostSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    likes = SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_likes(self, obj):
        return obj.likes.count()

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        post = Post.objects.create(author_id=user.id, **validated_data)
        return post
