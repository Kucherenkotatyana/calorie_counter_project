from django.db import models
from users.models import Customer


class CustomerActivity(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_add = models.DateTimeField()
    spent_calories = models.IntegerField()

    def __str__(self):
        return f"{self.customer} - {self.date_add} - {self.spent_calories}kcal"
