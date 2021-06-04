from django.db import models

# Create your models here.
class Text(models.Model):
    transcript=models.CharField(max_length=500000)
   
