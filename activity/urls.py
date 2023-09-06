from Calorie_counter.routers import OptionalSlashRouter
from activity.views import CustomerActivityViewSet, CustomerActivitySummarizeData
from django.urls import path


router = OptionalSlashRouter()
router.register(r'activities', CustomerActivityViewSet, basename='activity')
# Create: HTTP POST to /activities/
# Retrieve: HTTP GET to /activities/<pk>/
# Update: HTTP PUT/PATCH to /activities/<pk>/
# Delete: HTTP DELETE to /activities/<pk>/

urlpatterns = router.urls + [
    path('activities-list/', CustomerActivitySummarizeData.as_view(), name='activities-list'),
]
