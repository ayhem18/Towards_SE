from django.shortcuts import render

from django.http import HttpResponse, HttpRequest

from django.contrib.auth import authenticate


def home(req: HttpRequest) -> HttpResponse:
    return render(req, 
                  template_name='generic.html', 
                  context={"random_text":'yeye whasupp !!'} # empty context for the moment
                  )  



def login(req: HttpRequest) -> HttpResponse:
    user = req.user.is_authenticated
    if user: 
        # return the user page 
        return render()

    # check if the user is already log in
    return HttpResponse("empty res")
