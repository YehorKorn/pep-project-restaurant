import datetime
import time

from django import forms
from django.core.exceptions import ValidationError

from reservation.models import Reservation


class ReservationForm(forms.ModelForm):

    name = forms.CharField(
        error_messages={
            "required": "*"
        },
        widget=forms.TextInput(attrs={
            "placeholder": "Your Name",
            "class": "form-control",
            "autofocus": True,
        }))

    email = forms.EmailField(
        error_messages={
            "required": "*"
        },
        widget=forms.EmailInput(attrs={
            "placeholder": "Your Email",
            "class": "form-control",
        }))

    phone = forms.CharField(
        error_messages={
            "required": "*"
        },
        widget=forms.TextInput(attrs={
            "placeholder": "Your Phone",
            "class": "form-control",
        }))

    date_time = forms.CharField(
        error_messages={
            "required": "*",
            "invalid": "*Correct: 2023-06-28",
        },
        widget=forms.TextInput(attrs={
            "placeholder": "Date & Time",
            "class": "form-control datetimepicker-input",
            "data-toggle": "datetimepicker",
            "data-target": "#date3",
        }))

    CHOICES = (
        (1, 'People 1'),
        (2, 'People 2'),
        (3, 'People 3'),
        (4, 'People 4'),
    )
    number_of_people = forms.ChoiceField(
        choices=CHOICES,
        error_messages={
            "required": "*"
        },
        widget=forms.Select(attrs={
                    "placeholder": "No Of People",
                    "class": "form-select",
                })
    )

    special_request = forms.CharField(
        required=False,
        error_messages={
            "required": "*"
        },
        widget=forms.Textarea(attrs={
            "placeholder": "Description",
            "class": "form-control",
            "style": "height: 100px;"
        }))

    class Meta:
        model = Reservation
        fields = (
            "name",
            "email",
            "phone",
            "date_time",
            "number_of_people",
            "special_request",
        )

    def clean_date_time(self):
        date_time = self.cleaned_data["date_time"]
        date_time = datetime.datetime.strptime(date_time, "%m/%d/%Y %I:%M %p")
        if date_time + datetime.timedelta(minutes=1) <= datetime.datetime.now():
            raise ValidationError("*less then now!")
        return date_time


class ReservationSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Search by name...",
            "class": "form-control custom-search-input"
        })
    )

