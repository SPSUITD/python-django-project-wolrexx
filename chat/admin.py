from django.contrib import admin

from authorize.models import User
from .models import Dialog, Message

admin.site.register(User)
admin.site.register(Dialog)
admin.site.register(Message)
