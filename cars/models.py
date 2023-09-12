from django.db import models
# Create your models here.
class Car(models.Model):
    pic = models.ImageField(null= True, blank=True, upload_to='cars/')