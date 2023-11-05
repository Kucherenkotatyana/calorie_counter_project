from django.db import models
from django.core.validators import MinValueValidator
from users.models import Customer


class Meal(models.Model):
    BREAKFAST = "BR"
    LUNCH = "LU"
    DINNER = "DI"
    MEAL_CHOICES = [
        (BREAKFAST, "breakfast"),
        (LUNCH, "lunch"),
        (DINNER, "dinner")
    ]

    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_add = models.DateTimeField()
    meal_type = models.CharField(
        max_length=2,
        choices=MEAL_CHOICES
    )
    product_name = models.CharField(max_length=50)
    portion_size = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    portion_calories = models.FloatField()

    def __str__(self):
        return (f"{self.user} ate {self.portion_size}g/ml of {self.product_name} for {self.meal_type} "
                f"at {self.date_add}. Calories in the portion - {self.portion_calories}.")
