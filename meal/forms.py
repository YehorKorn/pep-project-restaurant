from django import forms
from django.core.exceptions import ValidationError

from meal.models import Meal, Category


class MealForm(forms.ModelForm):

    name = forms.CharField(
        error_messages={
            "required": "*"
        },
        widget=forms.TextInput(attrs={
            "placeholder": "Name meal",
            "class": "form-control",
            "autofocus": True,
        }))

    description = forms.CharField(
        error_messages={
            "required": "*"
        },
        widget=forms.Textarea(attrs={
            "placeholder": "Description",
            "class": "form-control",
            "style": "height: 100px;"
        }))

    CHOICES = (
        (1, 'People 1'),
        (2, 'People 2'),
        (3, 'People 3'),
        (4, 'People 4'),
    )
    people = forms.ChoiceField(
        choices=CHOICES,
        error_messages={
            "required": "*"
        },
        widget=forms.Select(attrs={
                    "placeholder": "Count people",
                    "class": "form-select",
                })
    )

    price = forms.DecimalField(
        error_messages={
            "required": "*"
        },
        widget=forms.NumberInput(attrs={
            "placeholder": "Price",
            "class": "form-control",
        }))

    preparation_time = forms.IntegerField(
        error_messages={
            "required": "*"
        },
        widget=forms.NumberInput(attrs={
            "placeholder": "Price",
            "class": "form-control",
        }))

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        error_messages={
            "required": "*"
        },
        widget=forms.Select(attrs={
            "placeholder": "Category",
            "class": "form-select",
        })
    )

    image = forms.ImageField(
        error_messages={
            "required": "*"
        },
        widget=forms.ClearableFileInput(attrs={
        })
    )

    slug = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Slug",
            "class": "form-control",
        }))

    class Meta:
        model = Meal
        fields = (
            "name",
            "description",
            "people",
            "price",
            "preparation_time",
            "category",
            "image",
            "slug",
        )

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price <= 0:
            raise ValidationError(" cannot be less than 0!")
        return price


class MealSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Search by name of meal..",
            "class": "form-control custom-search-input"
        })
    )
