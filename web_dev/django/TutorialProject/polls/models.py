from django.db import models

# Create your models here.

# the models are an abstraction of database tables
class Question(models.Model):
    # each of these attributes represents a column / field in the table
    question_text = models.CharField(max_length=200)
    publication_date = models.DateTimeField("Publication date")

class Choice(models.Model):
    # let's create a foreigh key
    question = models.ForeignKey(Question, # what table is this referring to (usually foreign keys are associated with primary keys form other tables, and not just the table itself ?? ) 
                                 on_delete=models.CASCADE # if the row associated with the question is removed from the 'Question' tale, so does the choice
                                 )
    # each of these attributes represents a column / field in the table
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    