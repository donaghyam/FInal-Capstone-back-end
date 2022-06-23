from django.db import models

class Ingredients(models.Model):
    
    type = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    alpha_acids = models.IntegerField(null=True)
    
    class Meta:
        ordering=['name']