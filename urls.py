# rest framework
from rest_framework.routers import DefaultRouter

# локальные импорты
from .views import AuthenticationViewSet

router = DefaultRouter()
router.register("auth", AuthenticationViewSet)
urlpatterns = router.urls
