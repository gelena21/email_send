from django.utils import timezone
from django.db import models

from users.models import User

NULLABLE = {
    "blank": True,
    "null": True,
}


class Client(models.Model):
    """Клиент - тот, кто получает рассылки"""

    email = models.EmailField(verbose_name="email")
    name = models.CharField(max_length=255, verbose_name="Ф. И. О.")
    comment = models.TextField(**NULLABLE, verbose_name="комментарий")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="пользователь", null=True
    )

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"

    def __str__(self):
        return f"{self.email}"


class Message(models.Model):
    subject = models.CharField(max_length=150, verbose_name="тема")
    body = models.TextField(verbose_name="текст")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        null=True, verbose_name="Пользователь сообщения"
    )

    def __str__(self):
        return f"{self.subject} {self.body}"

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщение"


class Mailing(models.Model):
    CHOICES_INTERVAL = [
        ("day", "единожды в день"),
        ("week", "единожды в неделю"),
        ("month", "единожды в месяц"),
    ]

    STATUS_CHOICES = [
        ("completed", "Завершено"),
        ("created", "Создано"),
        ("launched", "В работе"),
    ]

    title = models.CharField(max_length=255, verbose_name="заголовок рассылки")
    client = models.ManyToManyField(Client, verbose_name="клиенты")
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, null=True, verbose_name="сообщение"
    )
    start_date = models.DateTimeField(default=timezone.now,
                                      verbose_name="дата начала")
    next_date = models.DateTimeField(
        default=timezone.now, verbose_name="последующая дата"
    )
    end_date = models.DateTimeField(default=timezone.now,
                                    verbose_name="конечная дата")
    periodicity = models.CharField(
        default="единоразовая",
        max_length=64,
        choices=CHOICES_INTERVAL,
        verbose_name="периодичность",
    )
    status = models.CharField(
        max_length=64,
        choices=STATUS_CHOICES,
        verbose_name="статус рассылки",
        **NULLABLE,
    )
    is_active = models.BooleanField(default=True, verbose_name="актуальная")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name="пользователь", **NULLABLE
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ("start_date",)
        permissions = [("set_is_activated",
                        "Может менять активность рассылки")]


class Logs(models.Model):
    mailing = models.ForeignKey(Mailing,
                                on_delete=models.CASCADE,
                                verbose_name="рассылка", **NULLABLE)
    last_mailing_time = models.DateTimeField(auto_now=True,
                                             verbose_name="время "
                                                          "последней рассылки")
    status = models.CharField(max_length=50,
                              verbose_name="статус попытки рассылки",
                              null=True)
    response = models.CharField(max_length=300,
                                verbose_name="ответ сервера", **NULLABLE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_mailing_time = None

    def __str__(self):
        return f'{self.mailing}, {self.status}'

    class Meta:
        verbose_name = "лог"
        verbose_name_plural = "логи"
        