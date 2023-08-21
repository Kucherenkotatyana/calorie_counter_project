from .serializers import CustomerSerializer
from rest_framework import generics, permissions


class CustomerRegistrationView(generics.CreateAPIView):
    serializer_class = CustomerSerializer

    def perform_create(self, serializer):
        # Get the password from the request data
        password = self.request.data.get('password')

        # Create the user instance with a hashed password
        user = serializer.save()

        # Set the user's password securely using Django's authentication system
        user.set_password(password)
        user.save()


class CustomerDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    serializer_class = CustomerSerializer
