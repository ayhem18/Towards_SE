from django.contrib import admin

from .models import Blog, Tag

# these few lines enable adding and modifying records using the admin site
admin.site.register(Tag)
admin.site.register(Blog)

