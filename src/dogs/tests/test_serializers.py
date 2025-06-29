from django.db.models import Avg, Count
from django.test import TestCase

from dogs.models import Breed, Dog
from dogs.serializers import BreedSerializer, DogSerializer


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


class DogSerializerTestCase(TestCase):
    def setUp(self):
        self.breed = Breed.objects.create(
            name='Breed',
            size='t',
            friendliness=1,
            trainability=1,
            shedding_amount=1,
            exercise_needs=1,
        )

        self.dog = Dog.objects.create(
            name='Dog',
            age=10,
            breed=self.breed,
            gender='m',
            color='black',
            favorite_food='some food',
            favorite_toy='some toy',
        )

        self.expected_data = {
            'id': self.dog.id,
            'name': self.dog.name,
            'age': self.dog.age,
            'breed': self.dog.breed.id,
            'gender': self.dog.gender,
            'color': self.dog.color,
            'favorite_food': self.dog.favorite_food,
            'favorite_toy': self.dog.favorite_toy,
        }

    def test_create_ok(self):
        data = DogSerializer(self.dog).data

        self.assertEqual(self.expected_data, data)

    def test_create_ok_with_annotated(self):
        Dog.objects.create(
            name='Dog 2',
            age=20,
            breed=self.breed,
            gender='m',
            color='black',
            favorite_food='some food',
            favorite_toy='some toy',
        )

        dog_with_annotated = Dog.objects.annotate(
            avg_age=Avg('breed__dogs__age'),
            same_breed_count=Count('breed__dogs'),
        ).get(id=self.dog.id)

        data = DogSerializer(dog_with_annotated).data
        self.expected_data['avg_age'] = 15
        self.expected_data['same_breed_count'] = 2

        self.assertEqual(self.expected_data, data)
