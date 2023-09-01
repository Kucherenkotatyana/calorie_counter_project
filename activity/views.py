from .models import CustomerActivity
from .serializers import CustomerActivitySerializer
from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class CustomerActivityViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = CustomerActivity.objects.all()
    serializer_class = CustomerActivitySerializer
    permission_classes = [IsOwner, IsAuthenticated]
