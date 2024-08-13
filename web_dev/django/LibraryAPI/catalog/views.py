from django.shortcuts import render

from django.http import HttpRequest, HttpResponse
# Create your views here.

def all(req: HttpRequest) -> HttpResponse:

    return HttpResponse(content= "Mind your god damn business...")
