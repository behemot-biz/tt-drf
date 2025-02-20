from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from tt_drf_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer

"""
Views for the Profiles app.

This module provides API views for managing user profiles. It allows users
to retrieve a list of profiles, view detailed information about a specific
profile, and update their own profile. The views include support for filtering,
ordering, and permissions to ensure secure access control.

Classes:
    - ProfileList: Provides a list of user profiles, including aggregated
      counts for recipes, followers, and following. Supports filtering and
      ordering by various profile attributes.
    - ProfileDetail: Allows retrieval and updating of a specific profile.
      Updates are restricted to the profile owner via permissions.
"""


class ProfileList(generics.ListAPIView):
    """
    API view to retrieve a list of profiles.
    """
    queryset = Profile.objects.annotate(
        recipes_count=Count('owner__recipe', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile',
    ]
    ordering_fields = [
        'recipes_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    API view to retrieve or update a specific profile.
    """
    permission_classes = [IsOwnerOrReadOnly]
    # queryset = Profile.objects.all()
    queryset = Profile.objects.annotate(
        recipes_count=Count('owner__recipe', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
