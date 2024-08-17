from rest_framework.routers import SimpleRouter

from chatapp.users.api.views import AuthViewSet, ProfileViewSet

router = SimpleRouter()

router.register(
    prefix="auth",
    viewset=AuthViewSet,
    basename="auth"
)
router.register(
    prefix="profiles",
    viewset=ProfileViewSet,
    basename="profiles"
)

urlpatterns = [

              ] + router.urls
