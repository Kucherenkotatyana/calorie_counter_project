from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=50)
    calories = models.IntegerField()

    def __str__(self):
        return f"100 g/ml of {self.name} = {self.calories}kcal"
