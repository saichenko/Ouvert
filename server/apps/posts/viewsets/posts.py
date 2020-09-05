from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny

from url_filter.integrations.drf import DjangoFilterBackend

from apps.posts.serializers.posts import PostSerializer
from apps.posts.models.posts import Post
from apps.posts.permissions.posts import IsUserObjectOrReadOnly

from django.contrib.auth.models import User


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-created')
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('profile',)
    permission_classes = (IsUserObjectOrReadOnly,)

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            return (IsUserObjectOrReadOnly(),)
        elif self.request.method == 'POST':
            return (IsAuthenticated(), IsUserObjectOrReadOnly())
        else:
            return (AllowAny(),)

    def perform_create(self, serializer):
        return serializer.save(profile=self.request.user.profile.get())
