from datetime import datetime as dt
from typing import List, Tuple
from copy import copy

from django.db import IntegrityError

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Blog, Tag
from .serializers import BlogSerializer, TagSerializer

def home(req: HttpRequest) -> HttpResponse:
    return HttpResponse("this is the home page")


# let's first build an api that returns JsonResponse, instead of HttpResponse
def _get_all_blogs(request: HttpRequest) -> JsonResponse:
    _all_blogs = Blog.objects.all()

    return JsonResponse({"blogs": BlogSerializer(_all_blogs, many=True).data,
                         },
                        status=200)

def _get_blog_by_id(request: HttpRequest) -> JsonResponse:
    # get the id from the request
    try:
        return JsonResponse({
                            "blog": BlogSerializer(
                                            Blog.objects.get(
                                                    id=request.GET.get('id')
                                                    )
                                                ).data,                            
                            },
                            status=200
                        )

    # using the Model.objects.get throws an error:
    except Blog.DoesNotExist:
        return JsonResponse({"error": f"There is no such an id as: {int(request.GET.get('id'))}"},
                             status=404) 

def _get_blog_by_title(request: HttpRequest) -> JsonResponse:
    # get the id from the request
    try:
        return JsonResponse({
                            "blog": BlogSerializer(Blog.objects.get(title__exact=request.GET.get('title'))).data,                            
                            },status=200
                        )

    except Blog.DoesNotExist:
        return JsonResponse({"error": f"There is no such a title: {request.GET.get('title')}"},
                             status=404) 

def _get_blog_by_date(request: HttpRequest) -> JsonResponse:
    # there are two options: 
    date1 = request.GET.get('date1')
    date2 = request.GET.get('date2')

    if date2 is not None and date1 is None:
        return JsonResponse({"error": "Make sure that date1 is never null.", "date1": date1}, status=404)

    try:
        
        if date2 is not None:
            # the range fitering assumes [from, to]. 
            # check this useful link for working with dates in python 
            # https://www.w3schools.com/python/python_datetime.asp

            # reverse the dates if needed
            d1 = dt.strptime(date1, "%Y-%m-%d")
            d2 = dt.strptime(date2, "%Y-%m-%d")
            
            ds = [(d1, date1), (d2, date2)]
            ds = sorted(ds, key=lambda x: x[0])
            date1, date2 = ds[0][1], ds[1][1]

            # in this case find all blogs between the two datres
            return JsonResponse({"blogs": 
                                    BlogSerializer(
                                        Blog.objects.filter(created_at__range=[date1, date2]), # the range seems to include at least one end
                                        many=True
                                    ).data},status= 200
                                )

        # this line serves as a quick check for the date format. It will throw an error if the format is uncorrect.        
        d1 = dt.strptime(date1, "%Y-%m-%d")

        return JsonResponse({"blogs": BlogSerializer(
                                        Blog.objects.filter(created_at__exact=date1),
                                        many=True).data},
                            status=200
                            )                
    except ValueError: 
        return JsonResponse({"error": "Make sure dates are of the correct format: yyyy-mm-dd", "date1": date1, "date2": date2}, status= 404)

def _get_blog_by_tag(request: HttpRequest) -> JsonResponse:
    # find blogs that are associated with all the passed tags
    tags = request.GET.get('tags')
    if not isinstance(tags, (str, List, Tuple)):
        return JsonResponse({ 
                             "error":"Make sure to pass corret tags format a string or a sequence of strings", 
                             "tags": tags, 
                             "tags_type":type(tags)},
                                status= 404
                            )
    if isinstance(tags, str):
        tags = [tags]

    sol = Blog.objects.all()
    for t in tags:
        sol = sol.filter(tags__name__contains=t)

    return JsonResponse({"blogs": BlogSerializer(sol,
                                            many=True).data},
                                status= 200
                                )                

    
def _blog_get(request: HttpRequest) -> JsonResponse:
    if request.GET.get('id') is not None:
        return _get_blog_by_id(request)

    if request.GET.get('title') is not None:
        return _get_blog_by_title(request)

    if request.GET.get('date1') is not None:
        return _get_blog_by_date(request)

    if request.GET.get('tags') is not None:
        return _get_blog_by_tag(request)
    
    # the default is returning all blogs
    return _get_all_blogs(request)


def _blog_delete(request: HttpRequest) -> JsonResponse:
    pass

def _blog_patch(request: HttpRequest) -> JsonResponse:
    pass

def _blog_post(request: HttpRequest) -> JsonResponse:
    try:
        # ** easier than iterating through the field names myself ...
        # first fetch the tags we need
        # tags_objs = 

        # save a copy of the request parameters without the 'tags'
        req = copy(request.GET.dict())
        req.pop('tags')
 
        new_obj = Blog(**(req))

        # add the object to the data base
        new_obj.save()  

        # this code works if I only pass one tag id

        tags_request = request.GET.get('tags')

        tags_query_set = Tag.objects.filter(pk__in=tags_request)

        new_obj.tags.add(*tags_query_set)

        new_obj.save()


        return JsonResponse(data={"new_record": BlogSerializer(new_obj, many=False).data, "extra_info": request.GET.dict()}, 
                            status=201 # status for the correct post operation
                            )
    except KeyError:
        return JsonResponse(data={"error": "true", 
                                  "messsage": (f"some missing fields. Make sure the parameters {['title', 'author', 'price']}.  are all passed\n"
                                  f"Found: {request.GET}")
                                  }, 
                            status=400)


    except Tag.DoesNotExist:
        return JsonResponse(data={"error": "true", 
                                  "message": "At least one of the tags passed with the request is not present.",
                                  "request_content": request.GET.dict()
                                  }, 
                            status=400)
        
   
    except IntegrityError:
        return JsonResponse(data={"error": "true", 
                                  "messsage": (f"some missing fields. Make sure the parameters {['title', 'author', 'price']}.  are all passed\n"
                                  f"Found: {request.GET.dict()}")},
                            status=400)


@csrf_exempt
def blog(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        return _blog_get(request)

    if request.method == "DELETE":
        return _blog_delete(request) 

    if request.method == "PATCH":
        return _blog_patch(request) 

    if request.method == "POST":
        return _blog_post(request) 


def _get_all_tags(request: HttpRequest) -> JsonResponse:
    _all_tags = Tag.objects.all()

    return JsonResponse({"tags": [TagSerializer(b).data for b in _all_tags], "request_content": request.GET}, 
                        status=200)

def _post_tag(request: HttpRequest) -> JsonResponse:
    try:
        # ** easier than iterating through the field names myself ...
        new_obj = Tag(**request.GET.dict())        
        # add the object to the data base
        new_obj.save()

        return JsonResponse(data={"new_record": TagSerializer(new_obj, many=False).data, "extra_info": request.GET.dict()}, 
                            status=201 # status for the correct post operation
                            )
    except KeyError:
        return JsonResponse(data={"error": "true", 
                                  "messsage": (f"some missing fields. Make sure the parameters {['title', 'author', 'price']}.  are all passed\n"
                                  f"Found: {request.GET.dict()}")
                                  }, 
                            status=400)
    except IntegrityError as e:
        return JsonResponse(data={"error": "true", 
                                  "message": f"Integrity issues: {str(e)}",
                                  "request_content": request.GET.dict()},
                            status=400)

@csrf_exempt
def tag(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':    
        return _get_all_tags(request)

    if request.method == 'POST':
        return _post_tag(request)
