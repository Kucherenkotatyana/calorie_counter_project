from Calorie_counter.routers import OptionalSlashRouter
from activity.views import CustomerActivityViewSet


router = OptionalSlashRouter()
router.register(r'activities', CustomerActivityViewSet, basename='activity')
# Create: HTTP POST to /activities/
# Retrieve: HTTP GET to /activities/<pk>/
# Update: HTTP PUT/PATCH to /activities/<pk>/
# Delete: HTTP DELETE to /activities/<pk>/

urlpatterns = router.urls
