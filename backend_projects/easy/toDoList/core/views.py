from typing import Dict, Optional
import pprint

from django.shortcuts import render, redirect
from django.template import loader

from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status

from .models import User, Group, Task
from .serializers import GroupSerializer, TaskSerializer
 

def my_render(request:HttpRequest, template_name:str, context:Optional[Dict]=None):
    # the idea is simply to add the sanme fields to the context for links in the basic html to work properly
    if context is None:
        context = {}    

    context.update({"home_link": reverse('home_view'), 
                    "login_link": reverse('login_view'),
                    "register_link": reverse('register_user_view')
                    })

    return render(request, template_name=template_name, context=context)

def home(req: HttpRequest) -> HttpResponse:
    return my_render(req, template_name='generic.html')


# let's build an api for getting a user's specific information
def _get_user_tasks(request: HttpRequest) -> dict:
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

def _get_all_users(request: HttpRequest) -> JsonResponse:
    # get all users
    all_users = User.objects.all()
    print(all_users)
    return JsonResponse(data={"users": UserSerializer(all_users, many=True).data}, status=status.HTTP_200_OK)
    

@csrf_exempt
def account_json(request: HttpRequest) -> JsonResponse:
    if request.method != 'GET':

        return
    
    if 'username' not in request.GET:
        print("checking all users")
        return _get_all_users(request=request)
    
    try:
        # this function will raise User.DoesNotExist if the username in the request is not present in the dataset
        return JsonResponse(data={"groups": _get_user_tasks(request)},
                            status=status.HTTP_200_OK, 
                            )
    except User.DoesNotExist:
        return JsonResponse(data={"message": "there is no user"}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
def account_html(req: HttpRequest) -> HttpRequest:
    pp = pprint.PrettyPrinter(sort_dicts=True)
    # this is basically a version of the get_user function that returns a html page
    user_info = _get_user_tasks(req)
    pp.pprint(user_info)
    context = {"groups": [v for _, v in user_info.items()]}
    return my_render(req, 'tasks.html', context=context)



