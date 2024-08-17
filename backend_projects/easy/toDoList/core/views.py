from django.shortcuts import render

from django.http import HttpResponse, HttpRequest, JsonResponse
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

    # return tasks_serialized

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


@csrf_exempt
def login(req: HttpRequest) -> HttpResponse:
    user = req.user.is_authenticated
    print(user)    
    # if user:     
    #     print("The user is authenticated !!")
    #     # if the user is already logged in, redirect them to the get_user page
    #     # get the user information
    #     return account(req)

    return render(req, 'log_in.html', context={})



@csrf_exempt
def authenticate_user(req: HttpRequest) -> HttpRequest:
    username, password = req.GET['username'], req.GET['password']

    # authenticate
    try:
        user = authenticate(username=username, password=password)
        return account(user.username)

    except ValueError:
        print("The user was not authenticated")
        return render(req, 'log_in.html', context={})
        