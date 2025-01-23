from rest_framework import generics, permissions
from tt_drf_api.permissions import IsOwnerOrReadOnly
from .models import Like
from .serializers import LikeSerializer


class LikeList(generics.ListCreateAPIView):
    """
    API view to list all likes or create a new like.

    Permissions:
    - Authenticated users can create likes.
    - Read-only access for unauthenticated users.

    Attributes:
    - permission_classes: Defines the access control for the view.
    - serializer_class: Specifies the serializer to use for the Like model.
    - queryset: Retrieves all Like objects from the database.

    Methods:
    - perform_create: Associates the like with the current user.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDetail(generics.RetrieveDestroyAPIView):
    """
    API view to retrieve or delete a specific like.

    Permissions:
    - Only the owner of the like can delete it.

    Attributes:
    - permission_classes: Defines the access control for the view.
    - serializer_class: Specifies the serializer to use for the Like model.
    - queryset: Retrieves all Like objects from the database.
    """

    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
