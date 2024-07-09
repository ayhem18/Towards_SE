import os

from django.shortcuts import render # this is an easier way to work with template files
from django.http import HttpRequest, HttpResponse

import random
# Create your views here.
def about_view(request: HttpRequest) -> HttpResponse:
    # the path starts from the main project directory
    # let's pass some dynamic

    name = None
    if 'name' in request.GET:
        name = request.GET['name']
    
    id = None
    if 'id' in request.GET:
        id = request.GET['id']
    

    if not (name is None or id is None):
        info  = {"name": name, "id": id}
    else :
        info = {"name": "some_user", "id": "some_id"}
    
    info['values'] = [random.randint(1, 10) for _ in range(3)]

    return render(request, 
                  "about.html", # only pass the file name and not a complete path
                  info) # not passing a dictionary means that the file is static (requires no variables...)


