from django.urls import path

from main.apps import MainConfig
from main.views import (
    Index,
    MailingListView,
    MailingCreateView,
    MailingDeleteView,
    MailingDetailView,
    MailingUpdateView,
    MailingUpdateModeratorView,
    MessageListView,
    MessageCreateView,
    MessageUpdateView,
    MessageDeleteView,
    MessageDetailView,
    ClientListView,
    ClientCreateView,
    ClientUpdateView,
)

app_name = MainConfig.name

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("mailing/", MailingListView.as_view(), name="mailing_list"),
    path("mailing/create/", MailingCreateView.as_view(),
         name="mailing_create"),
    path(
        "mailing/detail/<int:pk>/", MailingDetailView.as_view(),
        name="mailing_detail"
    ),
    path(
        "mailing/update/<int:pk>/", MailingUpdateView.as_view(),
        name="mailing_update"
    ),
    path(
        "mailing_mod_edit/<int:pk>/",
        MailingUpdateModeratorView.as_view(),
        name="mailing_mod_edit",
    ),
    path(
        "mailing_delete/<int:pk>/", MailingDeleteView.as_view(),
        name="mailing_delete"
    ),
    path("message_list/", MessageListView.as_view(), name="message_list"),
    path("message_add/", MessageCreateView.as_view(), name="message_add"),
    path("message_edit/<int:pk>/", MessageUpdateView.as_view(),
         name="message_edit"),
    path("message_view/<int:pk>/", MessageDetailView.as_view(),
         name="message_view"),
    path(
        "message_delete/<int:pk>/", MessageDeleteView.as_view(),
        name="message_delete"
    ),
    path("clients/", ClientListView.as_view(), name="client_list"),
    path("client_add/", ClientCreateView.as_view(), name="client_add"),
    path("client_edit/<int:pk>", ClientUpdateView.as_view(),
         name="client_edit"),
]
