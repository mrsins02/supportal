from rest_framework.routers import SimpleRouter

from supportal.users.api.views import AuthViewSet, ProfileViewSet


router = SimpleRouter()

router.register(
    prefix="auth",
    viewset=AuthViewSet,
    basename="auth",
)
router.register(
    prefix="profiles",
    viewset=ProfileViewSet,
    basename="profiles",
)
