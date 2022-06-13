from django.db import models

class Styles(models.Model):
    
    label = models.CharField(max_length=30)