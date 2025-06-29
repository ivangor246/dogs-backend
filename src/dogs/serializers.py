from rest_framework import serializers

from dogs.models import Breed, Dog


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


class DogSerializer(serializers.ModelSerializer):
    """Serializer for the Dog model."""

    avg_age = serializers.IntegerField(read_only=True)
    same_breed_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Dog
        fields = (
            'id',
            'name',
            'age',
            'breed',
            'gender',
            'color',
            'favorite_food',
            'favorite_toy',
            'avg_age',
            'same_breed_count',
        )
