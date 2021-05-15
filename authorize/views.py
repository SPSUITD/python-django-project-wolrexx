from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.views import View

from .forms import AuthForm
from .models import User


def auth_view(request):
    if request.method == "POST":
        form = AuthForm(request.POST)
        if form.is_valid():
            user = form.save()
        else:
            user = User.get_or_none(
                login=form.data["login"], password=form.data["password"]
            )
            if not user:
                return HttpResponse("This user arleady exists")
        return set_cookies(user)

    return render(request, "auth_form.html", {"form": AuthForm()})


def set_cookies(user: User) -> HttpResponseRedirect:
    response = HttpResponseRedirect(f"/chat/")
    response.set_cookie("login", user.login)
    response.set_cookie("password", user.password)
    return response
