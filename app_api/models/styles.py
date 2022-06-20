from operator import mod
from django.db import models

class Styles(models.Model):
    
    label = models.CharField(max_length=30)
    image = models.CharField(null=True, max_length=400)
    
    class Meta:
        ordering=['label']