from typing import Dict, Optional
import pprint

from django.shortcuts import render

from django.http import HttpResponse, HttpRequest, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status

from .models import User, Group, Task
from .serializers import GroupSerializer, TaskSerializer

from django.views.generic.base import View, ContextMixin, TemplateResponseMixin, TemplateView, RedirectView


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


class MyTemplateView(View, ContextMixin, TemplateResponseMixin):
    template_name = 'test.html' # this attribute comes from the TemplateReponseMixin

    # try to use the field : extra_content instead of overrinding the get_context_data method
    extra_context = {"first_name": 'Ayhem', "last_name": "Bouabid"}

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['first_name'] = 'Ayhem'
    #     context['last_name'] = 'Bouabid'
    #     return context
    
    # if I am not mistaken the TempalteView class (django's) overrides the get function
    # and uses the context from 'ContextMixin' to populate the template 

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, template_name=self.template_name, context=self.get_context_data())


class V(TemplateView):
    template_name = 'test.html' # this attribute comes from the TemplateReponseMixin

    # try to use the field : extra_content instead of overrinding the get_context_data method
    extra_context = {"first_name": 'Ayhem', "last_name": "Bouabid"}


class MyRedirectView(RedirectView):
    # i need this view to use the parameters to build the final url
    query_string = True
    permanent = False
    url = reverse_lazy('account_json_view')

    # let's see if the view will redirect them correctly
