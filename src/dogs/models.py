from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Breed(models.Model):
    """Represents a dog breed with characteristic.

    Attributes:
        name (str): The name of the breed.
        size (str): The size category.
        friendliness (int): How friendly the breed is, from 1 to 5.
        trainability (int): How easy the breed is to train, from 1 to 5.
        shedding_amount (int): How much shedding, from 1 to 5.
        exercise_needs (int): Exercise requirements, from 1 to 5.
    """

    class Sizes(models.TextChoices):
        TINY = 't', 'Tiny'
        SMALL = 's', 'Small'
        MEDIUM = 'm', 'Medium'
        LARGE = 'l', 'Large'

    name = models.CharField(max_length=127)
    size = models.CharField(max_length=1, choices=Sizes.choices, default=Sizes.MEDIUM)
    friendliness = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    trainability = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    shedding_amount = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    exercise_needs = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])


class Dog(models.Model):
    """Represents a dog and its attributes.

    Attributes:
        name (str): The dog's name.
        age (int): The dog's age in years.
        breed (Breed): ForeignKey relation to the Breed model.
        gender (str): The dog's gender, male or female.
        color (str): The color of the dog.
        favorite_food (str): The dog's favorite food.
        favorite_toy (str): The dog's favorite toy.
    """

    class Genders(models.TextChoices):
        MALE = 'm', 'Male'
        FEMALE = 'f', 'Female'

    name = models.CharField(max_length=127)
    age = models.IntegerField()
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name='dogs')
    gender = models.CharField(max_length=1, choices=Genders.choices)
    color = models.CharField(max_length=30)
    favorite_food = models.CharField(max_length=127)
    favorite_toy = models.CharField(max_length=127)
