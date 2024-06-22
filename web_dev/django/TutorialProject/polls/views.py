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

def anotherView(request):
    return HttpResponse("Another View: shup up !!")


def say_hello(request):
    return HttpResponse("Hello Dear visitor !!")

def load_html(request):
    # load the template
    template = loader.get_template(os.path.join('polls', 'html_files', 'basic_index.html')) 
    return HttpResponse(template.render({}, request))
