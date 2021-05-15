from django.db import models


class User(models.Model):
    login = models.CharField("Юзернейм", max_length=30, unique=True)
    password = models.CharField("Пароль", max_length=40)

    photo = models.ImageField("Фотография пользователя", upload_to="user-avatars/")
    register_date = models.DateField("Дата регистрации", auto_now=True)

    def get_or_none(**kwargs):
        try:
            return User.objects.get(**kwargs)
        except:
            return None

    def __str__(self):
        return self.login

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
