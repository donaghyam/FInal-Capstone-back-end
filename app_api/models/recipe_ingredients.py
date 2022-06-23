from django.db import models
from django.contrib.auth.models import User

class RecipeIngredients(models.Model):
    
    ingredient = models.ForeignKey("Ingredients", on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    recipe = models.ForeignKey("Recipes", on_delete=models.CASCADE, related_name="recipe_ingredients")
    use = models.CharField(max_length=50)
    time = models.IntegerField(null=True)
    
    class Meta:
        ordering=['-time']