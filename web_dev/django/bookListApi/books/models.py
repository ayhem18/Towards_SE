from django.db import models


class Book(models.Model):
    # the class fields are as follows: 
    title = models.TextField(max_length=100, primary_key=True)
    author = models.TextField(max_length=20)
    price = models.IntegerField()  


    def __str__(self) -> str:
        return f"Book: {self.title}, written by {self.author}, priced at {self.price}"
    