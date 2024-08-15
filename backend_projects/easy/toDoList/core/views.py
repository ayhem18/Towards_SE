from django.shortcuts import render

from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status

from .models import User, Group
from .serializers import GroupSerializer

def home(req: HttpRequest) -> HttpResponse:
    return render(req, 
                  template_name='generic.html', 
                  context={"random_text":'yeye whasupp !!'} # empty context for the moment
                  )  


# let's build an api for getting a user's specific information
def _get_user(request: HttpRequest):
    try:
        username = request.GET.get('username')
        # get all groups and all tasks
        user_groups = Group.objects.filter(user__pk__exact=username)
        return JsonResponse({"groups": GroupSerializer(user_groups).data}, status=status.HTTP_200_OK)
    
    except: 
        return JsonResponse({"error": True, 
                             "message": "Something happended", 
                             "req_content": request.GET}, 
                            status=status.HTTP_200_OK)


@csrf_exempt
def get_user(request: HttpRequest) -> JsonResponse:
    try:
        username = request.GET.get('username')
        # get all groups and all tasks
        user_groups = Group.objects.filter(user__pk__exact=username)

        return JsonResponse(data=GroupSerializer(user_groups).data, status=status.HTTP_200_OK)

    except User.DoesNotExist: 
        return JsonResponse(data={"message": "there is no user with such username: "}, status=status.HTTP_404_NOT_FOUND)



def login(req: HttpRequest) -> HttpResponse:
    user = req.user.is_authenticated()
    if user: 
        # return the user page 
        return render()

