from django.shortcuts import render
from django.views import generic

from meal.models import Meal


class MealListView(generic.ListView):
    model = Meal


class MealDetailView(generic.DetailView):
    model = Meal
