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
