from django import forms
from django.forms import DateTimeInput, CheckboxInput

from main.models import Mailing, Message, Client


class StylingFormMixin(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name == "is_active":
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class MailingForm(StylingFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        user = self.request.user
        super().__init__(*args, **kwargs)
        self.fields["client"].queryset = Client.objects.filter(user=user)
        self.fields["message"].queryset = Message.objects.filter(user=user)

    class Meta:
        model = Mailing
        exclude = ("next_date", "user", "is_active")

        widgets = {
            "start_date": DateTimeInput(
                attrs={"placeholder": "ДД.ММ.ГГГГ ЧЧ:ММ:СС",
                       "type": "datetime-local"}
            ),
            "end_date": DateTimeInput(
                attrs={"placeholder": "ДД.ММ.ГГГГ ЧЧ: ММ:СС",
                       "type": "datetime-local"}
            ),
            "is_active": CheckboxInput(attrs={}),
        }


class MailingModerForm(StylingFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ("is_active",)


class MessageForm(StylingFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        exclude = ("user",)


class ClientForm(StylingFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ("user",)
        