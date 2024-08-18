from typing import Union


from django.http import QueryDict
from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from rest_framework import status

from .models import User, Group, Task
from .serializers import GroupSerializer, TaskSerializer

def home(req: HttpRequest) -> HttpResponse:
    return render(req, 
                  template_name='generic.html', 
                  context={"random_text":'yeye whasupp !!'} # empty context for the moment
                  )  


# let's build an api for getting a user's specific information
def _get_user(request: HttpRequest) -> dict:
    username = request.GET.get('username')
    # get all groups and all tasks
    user_groups = Group.objects.filter(owner__username__exact=username)

    groups_data = GroupSerializer(user_groups, many=True).data

    # gather all groups primary keys
    
    # save a mapping between the group ids and the group objects
    g_ids2objs = {g['id']: g for g in groups_data}

    # get all the tasks
    tasks = Task.objects.filter(group__in=list(g_ids2objs.keys()))

    tasks_serialized = TaskSerializer(tasks, many=True).data

    # tasks_serialized represents a list of dictionaries, each representing a task
    for t in tasks_serialized:
        # get the group id
        group_id = t['group']
        # add the task information
        if 'tasks' not in g_ids2objs[group_id]:
            g_ids2objs[group_id]['tasks'] = []

        # append the task representation to the group (without the group information)
        t.pop('group')
        g_ids2objs[group_id]['tasks'].append(t)

    # make sure each group has the field 'tasks'
    for g_id, g_value in g_ids2objs.items():
        if 'tasks' not in g_value:
            g_ids2objs[g_id]['tasks'] = []

    return g_ids2objs

@csrf_exempt
def get_user(request: HttpRequest) -> JsonResponse:
    try:
        # this function will raise User.DoesNotExist if the username in the request is not present in the dataset
        return JsonResponse(data={"groups": _get_user(request)},
                            status=status.HTTP_200_OK, 
                            )
    except User.DoesNotExist:
        return JsonResponse(data={"message": "there is no user"}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@login_required
def account(req: HttpRequest) -> HttpRequest:
    # this is basically a version of the get_user function that returns a html page
    return render(req, 'tasks.html', context=_get_user(req))



def _redirect_req2_user_account(req: HttpRequest) -> HttpResponseRedirect:
    # at this point the 'req' object has a url of http::/localhost/2dl/login (+ parameters)
    # some security concerns might pop up here, but that's secondary for now.
    # it needs to be redirected to http::/localhost/2dl/account/ with whatever parameters in the initial request
    # the following guide addresses this issue: https://realpython.com/django-redirects/#advanced-usage
    # extract the parameters from the initial url
    base_url = reverse('account_view')


    if 'username' not in req.GET:
        raise KeyError("the request is supposed to contain the parameter 'username'")

    # since req.POST / req.GET are implemented as QueryDict. They are immutable by default
    # we need a small turnaround to remove the QueryDict
    new_query_dict = QueryDict(req.GET.urlencode(), mutable=True)
    new_query_dict.pop('password')

    # I cannot remove the password key (I can make a turnaround this detail but it is secondary for now)
    # extract the query string from the request according to: https://stackoverflow.com/questions/11280948/best-way-to-get-query-string-from-a-url-in-python    
    query_string = new_query_dict.urlencode() # extracts a string with the parameters
    final_url = f'{base_url}?{query_string}' 
    return redirect(final_url)


@csrf_exempt
def login(req: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
    user = req.user.is_authenticated
    print(user)    

    if user:     
        return _redirect_req2_user_account(req=req)
    
    return render(req, 'log_in.html', context={})



@csrf_exempt
def authenticate_user(req: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
    username, password = req.GET['username'], req.GET['password']

    # set 
    user = authenticate(username=username, password=password)
    if user is None:
        print("The user was not authenticated")
        return render(req, 'log_in.html', context={})

    
    return _redirect_req2_user_account(req=req)
