from django.shortcuts import render
from django.views import generic

from meal.models import Meal


class MealListView(generic.ListView):
    model = Meal
    template_name = "menu.html"
    context_object_name = "meal_list"


class MealDetailView(generic.DetailView):
    model = Meal


def index(request):
    """View function for the home page of the site."""
    return render(request, "index.html")


def about(request):
    """View function for the home page of the site."""
    return render(request, "about.html")


def menu(request):
    """View function for the home page of the site."""
    return render(request, "menu.html")


def booking(request):
    """View function for the home page of the site."""
    return render(request, "booking.html")


def team(request):
    """View function for the home page of the site."""
    return render(request, "team.html")


def contact(request):
    """View function for the home page of the site."""
    return render(request, "contact.html")


def service(request):
    """View function for the home page of the site."""
    return render(request, "service.html")
