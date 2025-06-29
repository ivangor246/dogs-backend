from rest_framework.routers import SimpleRouter

from dogs.views import BreedViewSet

router = SimpleRouter()
router.register(r'breed', BreedViewSet, basename='breed')

urlpatterns = router.urls
