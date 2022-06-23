from django.db import models
from django.contrib.auth.models import User

class Recipes(models.Model):
    
    description = models.CharField(max_length=1000)
    name = models.CharField(max_length=50)
    style = models.ForeignKey("Styles", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    starting_gravity = models.DecimalField(max_digits=5, decimal_places=4)
    final_gravity = models.DecimalField(max_digits=5, decimal_places=4)
    abv = models.DecimalField(max_digits=5, decimal_places=3)
    ibu = models.IntegerField()
    srm = models.IntegerField()
    mash_ph = models.DecimalField(max_digits=5, decimal_places=2)
    batch_volume = models.DecimalField(max_digits=5, decimal_places=3)
    pre_boil_volume = models.DecimalField(max_digits=5, decimal_places=3)
    boil_time = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)