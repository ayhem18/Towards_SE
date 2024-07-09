from django.shortcuts import render

# Create your views here.
import os
from django.template import loader

# Create your views here.
from django.http import HttpResponse, HttpRequest

SCRITP_DIR = os.path.dirname(os.path.realpath(__file__))

# a view in Django is just a function after all 
# Django cannot determine which view to call 
# just by the function definition. Here comes the 'routing' process
# in other words mapping urls to views
def index(request: HttpRequest):
    # let's see if we can make this a little bit more complicated
    # It is easy to see that this does not scale and hence the use of "template for display purposes..."
    content = "<html><body><h1> this is a big ass header </h1></body></html>"
    return HttpResponse(content)

def get_user(request: HttpRequest, name: str, id: str):
    # let's see if we can make this a little bit more complicated
    # It is easy to see that this does not scale and hence the use of "template for display purposes..."
    content = f"<html><body><h1> this is a big ass header <br> The user {name} with id: {id} sent this request </h1></body></html>"
    return HttpResponse(content)


def get_user2(request: HttpRequest):
    if 'name' in request.GET:
        name = request.GET['name']
    else:
        name = 'unknown_name'

    if 'id' in request.GET:
        id = request.GET['id']
    else:
        id = 'unknown_id'

    content = f"<html><body><h1> this is a big ass header <br> The user {name} with id: {id} sent this request </h1></body></html>"
    return HttpResponse(content)


def home_view(request: HttpRequest):
    # first load the template
    template = loader.get_template('basic_index.html')
    context = {} # since no variables are expected in the html file
    return HttpResponse(template.render(context, request))
