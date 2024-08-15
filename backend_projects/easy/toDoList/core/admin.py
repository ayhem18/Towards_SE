from django.contrib import admin

# Register your models here.

from .models import Task, Group

admin.site.register(Task)
admin.site.register(Group)

# admin.site.register(User) # no need to register this model

