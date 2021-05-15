from typing import Union

from django.db import models
from authorize.models import User


class Dialog(models.Model):
    name = models.CharField("Нейм беседы", max_length=30)
    users = models.ManyToManyField(User, related_name="chats")

    photo = models.ImageField("Фотография диалога", upload_to="dialog-photos/")
    created_at = models.DateField("Дата создания", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Диалог"
        verbose_name_plural = "Диалоги"


class Message(models.Model):
    dialog = models.ForeignKey(Dialog, models.SET_NULL, "messages", null=True)
    at = models.ForeignKey(
        User, models.SET_NULL, "authored_messages", null=True
    )

    text = models.CharField("Текст сообщения", max_length=2048)
    date_send = models.DateTimeField("Дата отправки", auto_now=True)

    def __str__(self):
        return self.text

    def date(self) -> str:
        return self.date_send.strftime('%H:%M:%S %y.%m.%d')

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
