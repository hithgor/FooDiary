from django.db import models
from django.conf import settings


# Create your models here.

class CaloriesCard(models.Model): 
    #id = models.IntegerField()
    title = models.CharField(max_length=50)
    ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return self.id
    
class MealCard(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE
    )
    dateCreated = models.DateField()
    number = models.IntegerField()
    mealTitle = models.CharField(max_length=50)
    namesCalories = models.ManyToManyField('Ingredient')



class Ingredient(models.Model):
    #id = models.IntegerField()
    name = models.CharField(max_length=255)
    energy = models.IntegerField()

    def __str__(self):
        return self.name
