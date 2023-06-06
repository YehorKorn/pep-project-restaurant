from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic

from meal.models import Meal, Cook


class MealListView(generic.ListView):
    model = Meal
    template_name = "menu.html"
    context_object_name = "meal_list"
    queryset = Meal.objects.select_related("category")


class MealDetailView(generic.DetailView):
    model = Meal
    template_name = "meal/meal_detail.html"


class CookListView(generic.ListView):
    model = Cook
    template_name = "team.html"
    context_object_name = "cook_list"


def index(request):
    """View function for the home page of the site."""
    return render(request, "index.html")


def about(request):
    """View function for the about page of the site."""
    return render(request, "about.html")


def menu(request):
    """View function for the menu page of the site."""
    return render(request, "menu.html")


@login_required()
def booking(request):
    """View function for booking."""
    return render(request, "booking.html")


def contact(request):
    """View function for the contact page of the site."""
    return render(request, "contact.html")
