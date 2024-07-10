from django.shortcuts import render
from django.http import HttpRequest, JsonResponse, QueryDict
from django.db import IntegrityError

from django.views.decorators.csrf import csrf_exempt

from django.forms.models import model_to_dict
from .models import Book


def _book_get_request(request: HttpRequest) -> JsonResponse:
    
    
    all_books = Book.objects.all()
    
    # the idea here is to get all books
    return JsonResponse({"books": [model_to_dict(b) for b in all_books], "extra_info": request.GET}, 
                        status=200)

@csrf_exempt
def _book_post_request(request: HttpRequest) -> JsonResponse:
    try:
        
        obj = Book(request.GET.get('title'), request.GET.get('author'), request.GET.get('price'))
        
        # add the object to the data base
        obj.save()

        return JsonResponse(data={"new_record": model_to_dict(obj), "extra_info": request.GET.dict()}, 
                            status=201 # status for the correct post operation
                            )
    except KeyError:
        return JsonResponse(data={"error": "true", 
                                  "messsage": (f"some missing fields. Make sure the parameters {['title', 'author', 'price']}.  are all passed\n"
                                  f"Found: {request.GET}")
                                  }, 
                            status=400)
    except IntegrityError:
        return JsonResponse(data={"error": "true", 
                                  "messsage": (f"some missing fields. Make sure the parameters {['title', 'author', 'price']}.  are all passed\n"
                                  f"Found: {request.GET}")},
                            status=400)

@csrf_exempt
def _book_patch_request(request: HttpRequest) -> JsonResponse:
    
    try: 
        # make sure the book title is passed
        title = request.GET.get('title', None)
        if 'title' is None:
            return JsonResponse(data={"error": "true", "message": f"the patch method requires passing the book title. Request data: {request.GET}"}, status=400)

        field_names = [f.name for f in Book._meta.get_fields()]
        # iterate through the fields
        kvs = dict([(key, val) for key, val in request.GET.items() if key in field_names])


        # find the book with the title 
        book_qs = Book.objects.filter(pk=title)
        if len(book_qs) == 0:
            return JsonResponse(data={"error": "true", "message": f"the title: {title} requested is not available"}, status=404)

        book_qs.update(**kvs)               
        for book in book_qs:
            book.save() 

        return JsonResponse(data={"book": model_to_dict(book), "keys": list(kvs.keys())}, 
                            status=201 # status for the correct post operation
                            )
    # except KeyError:
    #     return JsonResponse(data={"error": "true", "messsage": f"some missing fields. Make sure the parameters {['title', 'author', 'price']} are all passed"}, 
    #                         status=400)
    except Book.DoesNotExist:
            return JsonResponse(data={"error": "true", "message": f"the title: {title} requested is not available"}, status=404)

    except IntegrityError:
        return JsonResponse(data={"error": "true", "messsage": "some issue with the passed data"}, status=400)
    

# view to return all books in the database
@csrf_exempt
def books(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        return _book_get_request(request=request)
    
    if request.method == 'POST':
        return _book_post_request(request=request)        

    if request.method == 'PATCH':
        return _book_patch_request(request=request)
