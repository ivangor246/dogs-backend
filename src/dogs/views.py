from django.db.models import Count
from rest_framework.viewsets import ModelViewSet

from dogs.models import Breed
from dogs.serializers import BreedSerializer


class BreedViewSet(ModelViewSet):
    """Introduces CRUD methods for interacting with breeds.

    Attributes:
        queryset (Queryset): A queryset of all breeds, annotated with dog count and ordered by id.
        serializer_class (Type[Serializer]): The serializer class for breed instances.
    """

    queryset = Breed.objects.all().annotate(dog_count=Count('dogs')).order_by('id')
    serializer_class = BreedSerializer
