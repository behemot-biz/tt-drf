from rest_framework import serializers
from .models import Profile
from followers.models import Follower

"""
Serializers for the Profiles app.

This module defines the ProfileSerializer, which is responsible for
serializing and deserializing Profile data. The serializer includes additional
fields for computed properties, such as counts for recipes, followers, and
following, as well as flags for ownership and following relationships.

Classes:
    - ProfileSerializer: Serializes Profile model data, including related
      metadata such as ownership status, following status, and aggregate counts.
"""


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner', 'following_id',
            'recipes_count', 'followers_count', 'following_count',
        ]
