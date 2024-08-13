from django.shortcuts import render

from django.http import HttpRequest, HttpResponse
# Create your views here.


def home(req: HttpRequest) -> HttpResponse:
    return HttpResponse("this is the home page")


def blog(req) -> HttpResponse:
    return HttpResponse("looking for a blog aren't you ?")
