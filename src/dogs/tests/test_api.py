from django.db.models import Avg, Count
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from dogs.models import Breed, Dog
from dogs.serializers import BreedSerializer, DogSerializer


class BreedViewSetTestCase(APITestCase):
    def setUp(self):
        self.breed_1 = Breed.objects.create(
            name='Breed 1',
            size='t',
            friendliness=1,
            trainability=1,
            shedding_amount=1,
            exercise_needs=1,
        )
        self.breed_2 = Breed.objects.create(
            name='Breed 2',
            size='s',
            friendliness=2,
            trainability=2,
            shedding_amount=2,
            exercise_needs=2,
        )

    def test_get(self):
        url = reverse('breed-list')
        response = self.client.get(url)
        serialized_data = BreedSerializer([self.breed_1, self.breed_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serialized_data, response.data)

    def test_get_with_dogs(self):
        Dog.objects.create(
            name='Dog',
            age=10,
            breed=self.breed_1,
            gender='m',
            color='black',
            favorite_food='Some food',
            favorite_toy='Some toy',
        )

        url = reverse('breed-list')
        response = self.client.get(url)
        breed_1_with_dogs = Breed.objects.annotate(dog_count=Count('dogs')).get(id=self.breed_1.id)
        serialized_data = BreedSerializer([breed_1_with_dogs, self.breed_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serialized_data, response.data)

    def test_get_one(self):
        url = reverse('breed-detail', args=[self.breed_1.id])
        response = self.client.get(url)
        serialized_data = BreedSerializer(self.breed_1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serialized_data, response.data)

    def test_create(self):
        url = reverse('breed-list')
        data = {
            'name': 'Breed 3',
            'size': 'm',
            'friendliness': 3,
            'trainability': 3,
            'shedding_amount': 3,
            'exercise_needs': 3,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(Breed.objects.count(), 3)
        self.assertEqual(Breed.objects.last().name, 'Breed 3')

    def test_update(self):
        url = reverse('breed-detail', args=[self.breed_1.id])
        updated_data = {
            'name': 'Updated breed',
            'size': 'l',
            'friendliness': 2,
            'trainability': 2,
            'shedding_amount': 1,
            'exercise_needs': 1,
        }
        response = self.client.put(url, updated_data, format='json')
        self.breed_1.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.breed_1.name, updated_data['name'])
        self.assertEqual(self.breed_1.size, updated_data['size'])
        self.assertEqual(self.breed_1.friendliness, updated_data['friendliness'])

    def test_delete(self):
        url = reverse('breed-detail', args=[self.breed_1.id])
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(Breed.objects.filter(id=self.breed_1.id).exists())


class DogViewSetTestCase(APITestCase):
    def setUp(self):
        self.breed = Breed.objects.create(
            name='Breed',
            size='t',
            friendliness=1,
            trainability=1,
            shedding_amount=1,
            exercise_needs=1,
        )

        self.dog_1 = Dog.objects.create(
            name='Dog',
            age=10,
            breed=self.breed,
            gender='m',
            color='black',
            favorite_food='some food',
            favorite_toy='some toy',
        )
        self.dog_2 = Dog.objects.create(
            name='Dog 2',
            age=20,
            breed=self.breed,
            gender='f',
            color='white',
            favorite_food='some food 2',
            favorite_toy='some toy 2',
        )

    def test_get(self):
        url = reverse('dog-list')
        response = self.client.get(url)

        dog_1_with_avg_age = Dog.objects.annotate(
            avg_age=Avg('breed__dogs__age'),
        ).get(id=self.dog_1.id)

        dog_2_with_avg_age = Dog.objects.annotate(
            avg_age=Avg('breed__dogs__age'),
        ).get(id=self.dog_2.id)

        serialized_data = DogSerializer([dog_1_with_avg_age, dog_2_with_avg_age], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serialized_data, response.data)

    def test_get_one(self):
        url = reverse('dog-detail', args=[self.dog_1.id])
        response = self.client.get(url)

        dog_with_same_breed_count = Dog.objects.annotate(
            same_breed_count=Count('breed__dogs'),
        ).get(id=self.dog_1.id)

        serialized_data = DogSerializer(dog_with_same_breed_count).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serialized_data, response.data)

    def test_create(self):
        url = reverse('dog-list')
        data = {
            'name': 'Dog 3',
            'age': 30,
            'breed': self.breed.id,
            'gender': 'm',
            'color': 'black',
            'favorite_food': 'some food 3',
            'favorite_toy': 'some toy 3',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(Dog.objects.count(), 3)
        self.assertEqual(Dog.objects.last().name, 'Dog 3')

    def test_update(self):
        url = reverse('dog-detail', args=[self.dog_1.id])
        updated_data = {
            'name': 'Updated dog',
            'age': 10,
            'breed': self.breed.id,
            'gender': 'm',
            'color': 'black',
            'favorite_food': 'some food 3',
            'favorite_toy': 'some toy 1',
        }
        response = self.client.put(url, updated_data, format='json')
        self.dog_1.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.dog_1.name, updated_data['name'])
        self.assertEqual(self.dog_1.age, updated_data['age'])
        self.assertEqual(self.dog_1.favorite_toy, updated_data['favorite_toy'])

    def test_delete(self):
        url = reverse('dog-detail', args=[self.dog_1.id])
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(Dog.objects.filter(id=self.dog_1.id).exists())
