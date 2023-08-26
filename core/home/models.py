from django.db import models

# Create your models here.

class Color (models.Model):
    Colour_name=models.CharField(max_length=100)
    def __str__(self):
        return self.Colour_name
class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='color',null=True,blank=True)
