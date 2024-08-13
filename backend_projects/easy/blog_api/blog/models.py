from django.db import models
from django.db.models.functions import Lower


# there are only two models in the initial version of the api

# characteristics of the Tag Model:
# 1. a unique set of values (constraint)
# 2. 

class Tag(models.Model):
    name = models.TextField(max_length=50, help_text="The name of the tag !!")

    class Meta: 
        ordering = ['name']
        # add a unique constraint
        constraints = [
            models.UniqueConstraint(
                Lower("name"), # the expression on which the constraint is enforced 
                name="unique_name_constraint", # the name of the constraint itself
                violation_error_message="The lower case name must be unique." # the message of the error thrown when the constraint is invalidated
            )
        ]


    def __str__(self):
        return self.name


class Blog(models.Model):
    # title, text, tag, date, id
    id = models.AutoField(verbose_name="blog_id", 
                          primary_key=True)

    title = models.CharField(max_length=100, 
                             null=False, 
                             blank=False)

    text = models.TextField() # the text itself can be quite large, so we use TextField

    tags = models.ManyToManyField(Tag) # the 

    created_at = models.DateField(null=False)

    class Meta: 
        ordering = ['created_at']

