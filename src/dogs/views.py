from django.db.models import Avg, Count
from rest_framework.viewsets import ModelViewSet

from dogs.models import Breed, Dog
from dogs.serializers import BreedSerializer, DogSerializer


class BreedViewSet(ModelViewSet):
    """Introduces CRUD methods for interacting with breeds.

    Attributes:
        queryset (Queryset): A queryset of all breeds, annotated with dog count and ordered by id.
        serializer_class (Type[Serializer]): The serializer class for breed instances.
    """

    queryset = Breed.objects.all().annotate(dog_count=Count('dogs')).order_by('id')
    serializer_class = BreedSerializer


class DogViewSet(ModelViewSet):
    """Introduces CRUD methods for interacting with dogs.

    Attributes:
        serializer_class (Type[Serializer]): The serializer class for dog instances.
    """

    serializer_class = DogSerializer

    def get_queryset(self):
        """Return a queryset of Dog instances with annotations depend on the current view action.

        Returns:
            QuerySet: A queryset of Dog objects, optionally annotated with:
                - `avg_age` for list views
                - `some_breed_count` for retrieve views
        """

        if self.action == 'list':
            return Dog.objects.annotate(avg_age=Avg('breed__dogs__age')).order_by('id')
        elif self.action == 'retrieve':
            return Dog.objects.annotate(same_breed_count=Count('breed__dogs')).order_by('id')
        return Dog.objects.all()
