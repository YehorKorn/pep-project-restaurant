from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from meal.models import Meal, Category


class CustomClearableFileInput(forms.ClearableFileInput):
    template_with_initial = '%(input)s'
    template_with_clear = '%(clear)s'

    def render(self, name, value, attrs=None, renderer=None):
        substitutions = {'input': super().render(name, value, attrs=attrs, renderer=renderer)}

        return self.template_with_initial % substitutions


class MealForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['image'].widget.attrs.update({'class': 'form-control'})

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
        required=False,
        error_messages={
            "required": "*"
        },
        widget=CustomClearableFileInput(attrs={
            # "class": "form-control",
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
        widget=forms.TextInput(attrs={"placeholder": "Search by model.."})
    )
