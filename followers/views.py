from rest_framework import generics, permissions
from tt_drf_api.permissions import IsOwnerOrReadOnly
from .models import Follower
from .serializers import FollowerSerializer


class FollowerList(generics.ListCreateAPIView):
    """
    API view to retrieve the list of followers or create a new follower.

    - GET: Returns a list of all followers.
    - POST: Allows an authenticated user to follow another user.

    Permissions:
        - Read-only for all users.
        - Write permissions are only for authenticated users.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()

    def perform_create(self, serializer):
        """
        Set the owner of the follower instance to the currently
        authenticated user.
        """
        serializer.save(owner=self.request.user)


class FollowerDetail(generics.RetrieveDestroyAPIView):
    """
    API view to retrieve or delete a specific follower relationship.

    - GET: Returns the details of a specific follower instance.
    - DELETE: Allows the owner of the follower instance to unfollow the user.

    Permissions:
        - Only the owner of the follower instance can delete it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()
