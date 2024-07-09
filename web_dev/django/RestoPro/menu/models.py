from django.db import models

# Create your models here.

class Dish(models.Model):
    # create the field
    _id = models.IntegerField(primary_key=True)
    name = models.TextField(max_length=30)    
    cuisine = models.TextField(max_length=20)
    def __str__(self):
        return f"dish: {self.name} from the {self.cuisine} cuisine"


class Menu(models.Model):
    menu_id = models.IntegerField(primary_key=True)
    def __str__(self):
        return f"Menu: {self.menu_id}"


class MenuIncludeDish(models.Model):
    # this Model represents a relation; whether a certain dish is a present in a certain menu
    menu_id = models.ManyToManyField(to=Menu)
    dish_id = models.ManyToManyField(to=Dish)

