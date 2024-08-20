from typing import Union, Dict, Optional

from django.shortcuts import render, redirect, resolve_url
from django.http import QueryDict

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required # the decorator is somehow 

from .forms import LoginForm, RegisterForm

from django.contrib.auth.views import LoginView

def my_render(request:HttpRequest, template_name:str, context:Optional[Dict]=None):
    # the idea is simply to add the sanme fields to the context for links in the basic html to work properly
    if context is None:
        context = {}    

    context.update({"home_link": reverse('home_view'), 
                    "login_link": reverse('login'), # the name of the django built-in login page is 'login'
                    "register_link": reverse('register_user_view')
                    })

    return render(request, template_name=template_name, context=context)

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
                return redirect(reverse('login'))
            
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
def login(req: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
    # the request is only a post request if it triggered by the submit button (which means the user is not authenticated)
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
                           "submit_url": reverse('login'), 
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
                           "submit_url": reverse('login'), 
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

    # check if the current user is authenticated
    if req.user.is_authenticated:
        print("The current user is authenticated")
        return _redirect_req2_user_account(req, user=req.user)

    print("The current user is not authenticated returning the login view!!")
    emtpy_form = LoginForm()
    context = {"form": emtpy_form, 
                "submit_url": reverse('login')}
    
    # if error is not None:
    #     print("the error field is not None")
    #     context['error'] = error
    
    return my_render(req, 'log_in.html', context=context)


## django provides a class to take care of standard authentication operations
# customizing it might be tricky
class MyLoginView(LoginView):
    # I am setting the fields according to the documentation of LoginView

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # redirect the user to the account view
        self.next_page = reverse_lazy('account_view')

        # use my form class
        self.form_class = LoginForm

    def get_successful_url(self):
        """Return the default redirect URL."""
        return resolve_url(self.next_page)
