from django.db import models

from django.contrib.auth.models import User


class Group(models.Model):
    name = models.CharField(verbose_name='group_name', max_length=50, help_text="A set of tasks grouped together")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, help_text='the user crating this set of tasks.')


# let's assume that the importance goes from 1 to 5

_task_importance = [(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)]

_task_status = [("N", "New"), ("I", "In progress"), ("D", "Done")]

class Task(models.Model):    
    # each task belongs to exactly one group of tasks
    group = models.ForeignKey(Group, on_delete=models.CASCADE, help_text="the id of the group the given task belongs to")
    name = models.CharField(max_length=50)

    importance = models.IntegerField(choices=_task_importance, help_text='assuming the importance can go from 1 to 5. The larger the number, the more important the task is')

    status = models.CharField(max_length=1, choices=_task_status, help_text="the status of the task")

    description = models.TextField(null=True, help_text='a description of the task, can be of any length')

    # date fields
    # created_at = models.DateField(null=False, blank=False) # it has to be filled 
    # deadline = models.DateField(null=True, blank=True) # there might be no set deadline for this task

    class meta: 
        ordering = ['importance', 'name']
            


