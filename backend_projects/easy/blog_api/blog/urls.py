from django.urls import include, path

from . import views


urlpatterns = [
    path("", views.home, name='home'),

    # the blog url will be used to  
    # 1. display all blogs  (using the GET http method)
    # 2. display blogs by filters (using the GET http method)
    # 3. create a new blog (using the POST http method)
    # 4. update a blog (using the PUT http method)
    # 5. delete ane existing blog (using the DELETE http method)
    path("blog/", views.blog, name='blog') 
]

