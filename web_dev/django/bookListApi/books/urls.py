from django.urls import include, path

from . import views

urlpatterns = [
    path("books", views.books, name='books'), 
    path("books_drf", views.books_drf, name='books_drf'), 
]


