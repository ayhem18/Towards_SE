from django.shortcuts import render

from django.http import HttpRequest, HttpResponse, JsonResponse

from django.views.decorators.csrf import csrf_exempt

from django.forms.models import model_to_dict
from .models import Blog, Tag

from .serializers import BlogSerializer, TagSerializer
from rest_framework.renderers import JSONRenderer

def home(req: HttpRequest) -> HttpResponse:
    return HttpResponse("this is the home page")


# let's first build an api that returns JsonResponse, instead of HttpResponse
def _get_all_blogs(request: HttpRequest) -> JsonResponse:
    _all_blogs = Blog.objects.all()

    # rest_framework rendered 
    jr = JSONRenderer()

    return JsonResponse({"blogs": BlogSerializer(_all_blogs, many=True).data,
                         "status": 200
                         })

    # return JsonResponse({"blogs": [jr.render(BlogSerializer(b).) for b in _all_blogs], "request_content": request.GET}, 
    #                     status=200)

    # return JsonResponse({"blogs": [model_to_dict(b) for b in _all_blogs], "request_content": request.GET}, 
    #                     status=200)


def _get_blog_by_id(request: HttpRequest) -> JsonResponse:
    # get the id from the request
    try:
        return JsonResponse({
                            "book": model_to_dict(Blog.objects.filter(id=request.GET.get('id'))), 
                            "status": 200
                            }
                        )

    except KeyError as e:
        return JsonResponse({"error": "The passed id does not exist", 
                             "status":404}) 

def _get_all_tags(request: HttpRequest) -> JsonResponse:
    _all_tags = Tag.objects.all()

    # the idea here is to get all books
    return JsonResponse({"tags": [TagSerializer(b).data for b in _all_tags], "request_content": request.GET}, 
                        status=200)

    # return JsonResponse({"tags": [model_to_dict(b) for b in _all_tags], "request_content": request.GET}, 
    #                     status=200)


# view to return all books in the database
@csrf_exempt
def blog(request: HttpRequest) -> JsonResponse:
    if request.GET.get('id') is None:
        return _get_all_blogs(request)
    return _get_blog_by_id(request)


@csrf_exempt
def tag(request: HttpRequest) -> JsonResponse:
    return _get_all_tags(request)

