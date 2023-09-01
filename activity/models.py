from django.db import models
from django.core.validators import MinValueValidator
from users.models import Customer


class CustomerActivity(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_add = models.DateTimeField()
    spent_calories = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = 'CustomerActivity'
        verbose_name_plural = 'CustomerActivities'

    def __str__(self):
        return f"{self.customer} - {self.date_add} - {self.spent_calories}kcal"
