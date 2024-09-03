from django.shortcuts import render

# let's get some views out of the way here
from django.http import HttpRequest, HttpResponse, JsonResponse 
from typing import Union

def main_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse(f"this is the main request. recived with query string: {request.GET.__dict__}")
