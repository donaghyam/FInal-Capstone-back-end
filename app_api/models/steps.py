from django.db import models

class Steps(models.Model):
    
    description = models.CharField(max_length=100)
    recipe = models.ForeignKey("Recipes", on_delete=models.CASCADE)
    temperature = models.IntegerField()
    time = models.IntegerField()
    amount = models.DecimalField(null = True, max_digits=4, decimal_places=1)