from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from customer_manager import CustomerManager


class Customer(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # custom manager
    objects = CustomerManager()

    # required for login
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
