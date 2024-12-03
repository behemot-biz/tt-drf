from rest_framework import serializers
from .models import Profile
from followers.models import Follower


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.

    This serializer provides:
        - Basic profile details such as `name`, `content`, and `image`.
        - Ownership information (`is_owner`) to determine if the current user
            owns the profile.
        - Follow status (`following_id`), which indicates if the current user
            is following this profile.
        - Aggregated counts for:
            - `recipes_count`: The number of recipes created by profile owner.
            - `followers_count`: The number of users following profile owner.
            - `following_count`: The number of users  profile owner follows.

    Methods:
        - `get_is_owner`:
            Determines if profile belongs to the currently authenticated user.
        - `get_following_id`:
            Retrieves the ID of the `Follower` relationship if the current
            user follows the profile owner.

    Attributes:
        - `model`: Specifies the Profile model being serialized.
        - `fields`: Defines fields exposed in the serialized representation.
    """
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
