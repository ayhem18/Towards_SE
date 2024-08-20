from typing import Union, Dict, Optional
import pprint


from django.http import QueryDict
from django.shortcuts import render, redirect
from django.template import loader

from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate
# from django.contrib.auth.decorators import login_required # the decorator is somehow 

from rest_framework import status

from .models import User, Group, Task
from .serializers import GroupSerializer, TaskSerializer, UserSerializer
from .forms import RegisterForm, LoginForm
 

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


def _redirect_req2_user_account(req: HttpRequest, user: User=None) -> HttpResponseRedirect:
    # at this point the 'req' object has a url of http::/localhost/2dl/login (+ parameters)
    # some security concerns might pop up here, but that's secondary for now.
    # it needs to be redirected to http::/localhost/2dl/account/ with whatever parameters in the initial request
    # the following guide addresses this issue: https://realpython.com/django-redirects/#advanced-usage
    # extract the parameters from the initial url
    base_url = reverse('account_view')

    if 'username' not in req.GET:
        if user is None:
            raise KeyError("the request is supposed to contain the parameter 'username'")

        new_query_dict = QueryDict(req.GET.urlencode(), mutable=True)
        new_query_dict['username'] = user.username
    else:    
        # since req.POST / req.GET are implemented as QueryDict. They are immutable by default
        # we need a small turnaround to remove the password information
        new_query_dict = QueryDict(req.GET.urlencode(), mutable=True)
        new_query_dict.pop('password')

    # extract the query string from the request according to: https://stackoverflow.com/questions/11280948/best-way-to-get-query-string-from-a-url-in-python    
    query_string = new_query_dict.urlencode() # extracts a string with the parameters
    final_url = f'{base_url}?{query_string}' 
    return redirect(final_url)


@csrf_exempt
def authenticate_user(req: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
    username, password = req.GET['username'], req.GET['password']

    # set 
    user = authenticate(username=username, password=password)
    if user is None:
        print("The user was not authenticated")
        return my_render(req, 'log_in.html')
    
    return _redirect_req2_user_account(req=req)


@csrf_exempt
def register_user(req: HttpRequest) -> HttpRequest:
    if req.method == "POST":
        filled_form = RegisterForm(req.POST)

        # validate the data
        if filled_form.is_valid():
            user_data = filled_form.cleaned_data.copy()
            user_data.pop('repeated_password')  

            username = user_data['username']
            # check if such a user exists in the database 
            try:
                User.objects.get(username=username)
                # redirect the user to the login page
                return redirect(reverse('login_view'))
            
            except User.DoesNotExist:
                # this means the user is not saved in the dataset
                pass

            # create a new user
            new_user = User.objects.create(**user_data)
            # save to the database
            new_user.save()

            # redirect the user to the account page
            return _redirect_req2_user_account(req=req, user=new_user)

        else:
            form = RegisterForm()

    else:
        form = RegisterForm()
        # the context is common between both request methods
        context = {"form": form, "submit_url": reverse('register_user_view')}
        return my_render(req, 'register.html', context=context)



@csrf_exempt
def login(req: HttpRequest, error=None) -> Union[HttpResponse, HttpResponseRedirect]:
    # assume logging is happening only through the form (kinda imposed by the code, no ?)
    if req.method == 'POST':
        filled_form = LoginForm(req.POST)
        
        if filled_form.is_valid():
            # authenticate the user
            user_name, pwd = filled_form.cleaned_data['username'], filled_form.cleaned_data['password']

            # check if the user is registered in the database
            try:
                User.objects.get(username=user_name)
            except User.DoesNotExist:           
                context = {"form": LoginForm(), 
                           "submit_url": reverse('login_view'), 
                           "error": f"There is no user with the {user_name} username. Create an account on our platform ?"}

                req.method = 'GET'

                req.POST = {} # not sure it is necessary, just trying to think about the data passed through the request
                return my_render(req, template_name='log_in.html', context=context)

            # authenticate
            user = authenticate(username=user_name, password=pwd)

            if user is None:
                # the user exists but the password is wrong
                print("the suer is not authenticated")
                context = {"form": filled_form, 
                           "submit_url": reverse('login_view'), 
                           "error": f"Incorrect Password. Please try again !!!"}

                # make sure the method is set to GET
                req.method = 'GET'
                req.POST = {}

                return my_render(req, 'log_in.html', context=context)

            print("the user is authenticated")
            return _redirect_req2_user_account(req, user=user)

        else:
            emtpy_form = LoginForm()
            context = {"form": emtpy_form, 
                       "submit_url": reverse('register_user_view'), 
                       "context":{"error": filled_form.errors}}
            return my_render(req, 'log_in.html', context=context)



    print("the server recieved a 'get' request")
    # create an empty form

    emtpy_form = LoginForm()
    context = {"form": emtpy_form, 
                "submit_url": reverse('login_view')}
    
    if error is not None:
        print("the error field is not None")
        context['error'] = error
    
    print("return the login view") 
    return my_render(req, 'log_in.html', context=context)
