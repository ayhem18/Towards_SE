from django.db import models

# Create your models here.



class CuisineCategory(models.Model):
    # the idea here is to create categories of dishes
    category_id = models.IntegerField(primary_key=True)
    category_name = models.TextField(max_length=30)

    def __str__(self) -> str:
        return f"Category: {self.category_name}, id: {self.category_id}"


class Dish(models.Model):
    # create the field
    id = models.IntegerField(primary_key=True)
    name = models.TextField(max_length=30)    
    
    # each dish belongs to a single category (However, a category is associated with many dishes)
    # the category id should be foreign key in the Dish relation

    # as long as there is one dish belonging to the category, the category cannot be deleted 
    category_id = models.ForeignKey(to=CuisineCategory, on_delete=models.PROTECT)


# a menu is somewhat independent of a category
class Menu(models.Model):
    menu_id = models.IntegerField(primary_key=True)
    def __str__(self):
        return f"Menu: {self.menu_id}"


class MenuIncludeDish(models.Model):
    # this Model represents a relation; whether a certain dish is a present in a certain menu
    menu_id = models.ManyToManyField(to=Menu)
    dish_id = models.ManyToManyField(to=Dish)

