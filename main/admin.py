from django.contrib import admin
from main.models import Client, Message, Mailing, Logs


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    pass


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = (
        "mailing",
        "last_mailing_time",
        "status",
    )
