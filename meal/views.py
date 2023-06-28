from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic, View

from meal.forms import MealForm, MealSearchForm
from meal.models import Meal, Cook, Category


class MealListView(generic.ListView):
    model = Meal
    template_name = "meal/menu.html"
    context_object_name = "meal_list"
    # paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MealListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = MealSearchForm(initial={
            "name": name
        })

        context["categories"] = Category.objects.all().order_by("pk")

        return context

    def get_queryset(self):
        queryset = Meal.objects.select_related("category")
        form = MealSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class MealDetailView(generic.DetailView):
    model = Meal
    template_name = "meal/meal_detail.html"


class MealUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = Meal
    form_class = MealForm
    template_name = "meal/meal_form.html"

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser


class MealCreateView(UserPassesTestMixin, generic.CreateView):
    model = Meal
    form_class = MealForm
    template_name = "meal/meal_form.html"
    success_url = reverse_lazy("meal:menu")

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser


class MealDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = Meal
    success_url = reverse_lazy("meal:menu")

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser


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
    return render(request, "meal/menu.html")


def contact(request):
    """View function for the contact page of the site."""
    return render(request, "contact.html")
