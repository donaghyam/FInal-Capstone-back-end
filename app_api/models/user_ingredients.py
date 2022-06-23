from django.db import models
from django.contrib.auth.models import User

class UserIngredients(models.Model):
    
    ingredient = models.ForeignKey("Ingredients", on_delete=models.CASCADE, related_name="user_ingredients")
    quantity = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering=['quantity']