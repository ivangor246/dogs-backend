from django.db.models import Count
from django.test import TestCase

from dogs.models import Breed, Dog
from dogs.serializers import BreedSerializer


class BreedSerializerTestCase(TestCase):
    def setUp(self):
        self.breed = Breed.objects.create(
            name='Breed',
            size='t',
            friendliness=1,
            trainability=1,
            shedding_amount=1,
            exercise_needs=1,
        )

        self.expected_data = {
            'id': self.breed.id,
            'name': self.breed.name,
            'size': self.breed.size,
            'friendliness': self.breed.friendliness,
            'trainability': self.breed.trainability,
            'shedding_amount': self.breed.shedding_amount,
            'exercise_needs': self.breed.exercise_needs,
            'dog_count': 0,
        }

    def test_create_ok(self):
        data = BreedSerializer(self.breed).data

        self.assertEqual(self.expected_data, data)

    def test_create_ok_with_dogs(self):
        Dog.objects.create(
            name='Dog',
            age=10,
            breed=self.breed,
            gender='m',
            color='black',
            favorite_food='Some food',
            favorite_toy='Some toy',
        )

        breed_with_dogs = Breed.objects.annotate(dog_count=Count('dogs')).get(id=self.breed.id)

        data = BreedSerializer(breed_with_dogs).data
        self.expected_data['dog_count'] = 1

        self.assertEqual(self.expected_data, data)
