"""
In this script, I experiment with the django rest framework api toolkit
"""

from datetime import datetime as dt
from typing import List, Tuple
from copy import copy

from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy

from rest_framework import status # used for more readable error codes
from rest_framework.decorators import api_view 

# request and response classes with more functionalities than the django ones
from rest_framework.response import Response  

from .serializers import BlogSerializer, TagSerializer
from .models import Blog, Tag
from .forms import TagForm

def home(req):
    return HttpResponse("this is the home page")


def _get_all_blogs(request:HttpRequest) -> Response:
    # render the data 
    _all_blogs = Blog.objects.all()
    return JsonResponse({"blogs": BlogSerializer(_all_blogs, many=True).data, "req_content": request.GET,
                         },
                        status=status.HTTP_200_OK # this status is much better than the usual 200
                        )

def _get_blog_by_id(request :HttpRequest) -> JsonResponse:
    # get the id from the request
    try:
        return JsonResponse({
                            "blog": BlogSerializer(
                                            Blog.objects.get(
                                                    id=request.GET.get('id')
                                                    )
                                                ).data,                            
                            },
                            status=status.HTTP_200_OK
                        )

    # using the Model.objects.get throws an error:
    except Blog.DoesNotExist:
        return JsonResponse({"error": f"There is no such an id as: {int(request.GET.get('id'))}"},
                             status=404) 

def _get_blog_by_title(request :HttpRequest) -> JsonResponse:
    # get the id from the request
    try:
        return JsonResponse({
                            "blog": BlogSerializer(Blog.objects.get(title__exact=request.GET.get('title'))).data,                            
                            },status=status.HTTP_200_OK
                        )

    except Blog.DoesNotExist:
        return JsonResponse({"error": f"There is no such a title: {request.GET.get('title')}"},
                             status=404) 

def _get_blog_by_date(request :HttpRequest) -> JsonResponse:
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
                                    ).data},
                                status=status.HTTP_200_OK
                            )

        # this line serves as a quick check for the date format. It will throw an error if the format is uncorrect.        
        d1 = dt.strptime(date1, "%Y-%m-%d")

        return JsonResponse({"blogs": BlogSerializer(
                                        Blog.objects.filter(created_at__exact=date1),
                                        many=True).data},
                            status=status.HTTP_200_OK
                            )                
    except ValueError: 
        return JsonResponse({"error": "Make sure dates are of the correct format: yyyy-mm-dd", "date1": date1, "date2": date2}, status= 404)

def _get_blog_by_tag(request :HttpRequest) -> JsonResponse:
    # find blogs that are associated with all the passed tags
    tags = request.GET.get('tags')
    if not isinstance(tags, (str, List, Tuple)):
        return JsonResponse({ 
                             "error":"Make sure to pass corret tags format a string or a sequence of strings", 
                             "tags": tags, 
                             "tags_type":type(tags)},
                                status=404
                            )
    if isinstance(tags, str):
        tags = [tags]

    sol = Blog.objects.all()
    for t in tags:
        sol = sol.filter(tags__name__exact=t)

    return JsonResponse({"blogs": BlogSerializer(sol,
                                            many=True).data},
                                status=status.HTTP_200_OK
                                )                

# import json
# request = json.loads(request.body)

def _blog_post(request: HttpRequest) -> JsonResponse:

    try:
        req = copy(request.POST)

        if 'tags' not in req:
            return JsonResponse({"error": "true", "message": "The 'tags' field is required", "req_content": request }, status=status.HTTP_400_BAD_REQUEST)                

        # remove the 'tags' field
        req.pop('tags')

        serializer = BlogSerializer(data=req.dict())
        if not serializer.is_valid():
            error_dict = copy(serializer.errors)
            error_dict['_source'] = 'BlogSerializer'
            return JsonResponse(error_dict, status=status.HTTP_400_BAD_REQUEST)

        # save the object to the database
        serializer.save()

        # this code works if I only pass one tag id
        tags_request = request.POST.get('tags')
        
        if not isinstance(tags_request, (List, Tuple)):
            tags_request = [tags_request]        

        # make sure each tags passed exists in the database
        for t in tags_request:
            try:
                Tag.objects.get(pk=t)
            except Tag.DoesNotExist:
                return JsonResponse(data={"error": "true", 
                                        "message": f"There is no tag with id: {t}",
                                        "request_content": request.POST
                                        }, 
                                    status=status.HTTP_400_BAD_REQUEST)

        tags_query_set = Tag.objects.filter(pk__in=tags_request)

        serializer.update(serializer.instance, {'tags': tags_query_set})
        # save the model again 
        serializer.save()

        return JsonResponse(data={"new_record": serializer.data, "req_content": request.POST}, 
                            status=201 # status for the correct post operation
                            )
   
    except IntegrityError as e:
        return JsonResponse(data={"error": "true", "message": str(e)},
                            status=400)


def _blog_get(request :HttpRequest) -> JsonResponse:
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


@csrf_exempt
@api_view(['GET', 'POST']) # this means that this view can only recieve HTTP GET, POST requests
def blog(request :HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        return _blog_get(request)

    if request.method == "POST":
        return _blog_post(request) 

def _get_all_tags(request :HttpRequest) -> JsonResponse:
    _all_tags = Tag.objects.all()

    return JsonResponse({"tags": [TagSerializer(b).data for b in _all_tags], "request_content": request.GET}, 
                        status=200)

def _post_tag(request :HttpRequest) -> JsonResponse:
    try:
        # create a serializer out of the request data
        serializer = TagSerializer(**request.GET)
        
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # save the object
        serializer.save()

        return JsonResponse(data={"new_record": serializer.data, "extra_info": request.GET}, 
                            status=201 # status for the correct post operation
                            )
    except IntegrityError as e:
        return JsonResponse(data={"error": "true", 
                                  "message": f"Integrity issues: {str(e)}",
                                  "request_content": request.GET},
                            status=400)

def tag(request :HttpRequest) -> JsonResponse:
    if request.method == 'GET':    
        return _get_all_tags(request)

    if request.method == 'POST':
        return _post_tag(request)


from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, CreateView

class TagViewByName(DetailView):
    model = Tag
    slug_field = 'name' 
    slug_url_kwarg = 'name'

    def get(self, request, *args, **kwargs):
        try:
            return JsonResponse({
                            "tag": TagSerializer(self.get_object()).data,                            
                            },status=status.HTTP_200_OK
                        )
        except Exception as e:            
            return JsonResponse({"error": f"{e}"},
                                status=404) 





# let's try to understand how to work with django Detail and List views            
class BlogViewByTitle(DetailView):
    model = Blog
    slug_field = 'title' 
    slug_url_kwarg = 'title'

    def get(self, request, *args, **kwargs):
        try:
            return JsonResponse({
                            "blog": BlogSerializer(self.get_object()).data,                            
                            },status=status.HTTP_200_OK
                        )
        except Blog.DoesNotExist:
            return JsonResponse({"error": f"Title {kwargs['title']} does not exist"},
                                status=404) 
        except Exception as e:            
            return JsonResponse({"error": f"{e}"},
                                status=404) 


class BlogView(ListView):
    # apparently a Listview only supports displaying all values with no filtering...
    # but it takes care of pagination (which is really great ...)
    # can be used for filtering purposes when overriding the get_object_list method
    model = Blog
    paginate_by = 2
    ordering = 'id'  # order by id

    def get(self, request, *args, **kwargs):
        # this code is copied from the get_context_data method  
        queryset = self.get_queryset() # override this function to add filtering
        # extract the number of items per page
        page_size = self.get_paginate_by(queryset)
        # paginate
        _, _, data, _ = self.paginate_queryset(
            queryset, page_size
        )   

        p = kwargs.get(self.page_kwarg, 1)  

        return JsonResponse(data={f"blogs_page_{p}":BlogSerializer(data, many=True).data}, 
                            status=status.HTTP_200_OK)


def blog_view_paginated(req, *args, **kwargs):
    return BlogView.as_view(paginate_by=kwargs['paginate_by'])(req, **kwargs)


# let's create, update and delete some tags
class CreateTag(CreateView):
    # the idea here is quite simple
    template_name = 'tag_form.html'    
    form_class = TagForm
    
    # let's override the get_successful_url()
    def get_success_url(self) -> str:
        # since get_successful_url is called only after form.is_valid is correct
        # the self.object should be present at this point
        
        base_url =reverse_lazy('all_tags_view')
        print("issue at the reverse_lazy level")
        tag_name = self.object.name

        print("the url is ready!!")
        url = "{}/{}".format(base_url, tag_name)
        print(url)
        return url
