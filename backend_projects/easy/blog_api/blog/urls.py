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
    # path("blog/", views.blog, name='blog'), 

    path("blog/<slug:title>/", views.BlogViewByTitle.as_view(), name='blog_by_title_view'), # redirect any request to filter blogs by title
    path("all/<int:page>/", views.BlogView.as_view(), name='all_blogs_page_view'), # redirect any request to filter blogs by title
    path("all/", views.BlogView.as_view(), name='all_blogs_view'), # return all blogs paginated (some fixed number of blogs per page)
    path("all/<int:paginate_by>/<int:page>", views.blog_view_paginated, name='all_blogs_paginated_page_view'), # return all blogs while setting the number of books per page

    path("tag", views.tag, name='all_tags_view'), 
    path("tag/create", views.CreateTag.as_view(), name='create_tag_view'), 
    path("tag/<slug:name>", views.TagViewByName.as_view(), name='tag_by_name_view'), 
    
]

