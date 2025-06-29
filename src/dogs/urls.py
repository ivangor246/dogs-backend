from rest_framework.routers import SimpleRouter

from dogs.views import BreedViewSet, DogViewSet

router = SimpleRouter()
router.register(r'breed', BreedViewSet, basename='breed')
router.register(r'dog', DogViewSet, basename='dog')

urlpatterns = router.urls
