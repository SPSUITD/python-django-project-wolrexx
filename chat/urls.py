from django.urls import path
from . import views


urlpatterns = [
    path("user/<str:username>", views.user_detail_info, name="user-info"),
    path("chat/", views.dialog_list_view, name="user-dialogs"),
    path("chat/<slug:chat>/", views.dialog_detail_view, name="dialog")
]
