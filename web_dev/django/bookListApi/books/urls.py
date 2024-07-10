from django.urls import include, path

from . import views

urlpatterns = [
    path("books", views.books, name='books'), 
]


