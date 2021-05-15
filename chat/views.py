from django.shortcuts import render, HttpResponse

from authorize.models import User
from .models import Dialog, Message


def user_detail_info(request, username: int):
    if "login" in request.COOKIES and "password" in request.COOKIES:
        user = User.get_or_none(login=username, password=request.COOKIES["password"])
        if user:
            return render(request, "user_detail.html", {"user": user})

    return HttpResponse("Access denied")


def dialog_list_view(request):
    """ Список чатов """
    user = User.get_or_none(login=request.COOKIES.get("login"))
    if user is None:
        return HttpResponse("You are not loggend in")

    return render(
        request, "chat/chat_list.html",
        {"my_name": user.login, "dialogs": user.chats})


def dialog_detail_view(request, chat: str):
    """ Чат """
    data = {"login": request.COOKIES.get("login"), "password": request.COOKIES.get("password")}

    user = User.get_or_none(**data)
    chat = user.chats.filter(name=chat).first()

    if user is None or not chat:
        return HttpResponse("You not authorize or Chat not exists")

    return render(request, "chat/chat.html", {"dialog": chat, "user": user})
