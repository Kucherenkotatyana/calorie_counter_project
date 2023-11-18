from django.db import models
from django.core.validators import MinValueValidator
from users.models import Customer


class CustomerProfile(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    target = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.customer} has a target of {self.target}kcal for a day"
