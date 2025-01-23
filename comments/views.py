from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from tt_drf_api.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer


class CommentList(generics.ListCreateAPIView):
    """
    API view to retrieve a list of comments or create a new comment.

    - Allows authenticated users to create comments.
    - Anyone can view the list of comments.
    - Filters comments by associated recipe using query parameters.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['recipe']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific comment.

    - Allows the owner of the comment to update or delete it.
    - Anyone can view the comment.
    - Ensures object-level permissions using the IsOwnerOrReadOnly permission.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()
