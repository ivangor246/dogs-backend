from rest_framework import serializers

from dogs.models import Breed


class BreedSerializer(serializers.ModelSerializer):
    """Serializer for the Breed model."""

    dog_count = serializers.IntegerField(default=0, read_only=True)

    class Meta:
        model = Breed
        fields = (
            'id',
            'name',
            'size',
            'friendliness',
            'trainability',
            'shedding_amount',
            'exercise_needs',
            'dog_count',
        )
