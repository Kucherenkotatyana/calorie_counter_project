from .serializers import CustomerSerializer
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status


class CustomerRegistrationView(generics.CreateAPIView):
    serializer_class = CustomerSerializer

    def perform_create(self, serializer):
        # Get the password from the request data
        password = self.request.data.get('password')

        # Create the user instance with a hashed password
        user = serializer.save()

        # Set the user's password securely using Django's authentication system
        user.set_password(password)

        if serializer.is_valid():
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    serializer_class = CustomerSerializer
