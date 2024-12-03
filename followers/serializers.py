from django.db import IntegrityError
from rest_framework import serializers
from .models import Follower


class FollowerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Follower model.

    Fields:
        - `id`: The unique identifier of the follower instance.
        - `created_at`: The timestamp when the follow relationship was
                        created.
        - `owner`: The username of the user who created the follow
                    relationship.
        - `followed`: The ID of the user being followed.
        - `followed_name`: The username of the user being followed.

    Behavior:
        - Prevents users from following themselves.
        - Ensures that duplicate follow relationships cannot be created.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    followed_name = serializers.ReadOnlyField(source='followed.username')

    class Meta:
        model = Follower
        fields = [
            'id', 'created_at', 'owner', 'followed', 'followed_name'
        ]

    def create(self, validated_data):
        """
        Create a new Follower instance.

        Validations:
            - Ensure the user is not trying to follow themselves.
            - Ensure the follow relationship is unique.

        Args:
            validated_data (dict): The data validated by the serializer.

        Returns:
            Follower: The created Follower instance.

        Raises:
            serializers.ValidationError:
                If the user tries to follow themselves or if the follow
                relationship already exists.
        """
        if validated_data['owner'] == validated_data['followed']:
            raise serializers.ValidationError({
                'detail': 'You cannot follow yourself.'
            })
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'Already following this user.'
            })
