from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic, View

from meal.forms import MealForm, MealSearchForm
from meal.models import Meal, Cook


class MealListView(generic.ListView):
    model = Meal
    template_name = "meal/menu.html"
    context_object_name = "meal_list"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MealListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = MealSearchForm(initial={
            "name": name
        })

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


class MealUpdateView(generic.UpdateView):
    model = Meal
    form_class = MealForm
    template_name = "meal/meal_form.html"


class MealCreateView(LoginRequiredMixin, generic.CreateView):
    model = Meal
    form_class = MealForm
    template_name = "meal/meal_form.html"
    success_url = reverse_lazy("meal:menu")


class MealDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Meal
    success_url = reverse_lazy("meal:menu")


# class MealDeleteView(View):
#
#     def get(self, request, meal_slug):
#         meal = Meal.objects.get(slug=meal_slug)
#         return render(request, 'meal/meal_form.html', {'meal': meal})
#
#     def post(self, request, meal_slug):
#         meal = Meal.objects.get(slug=meal_slug)
#         meal.delete()
#         return redirect('meal:menu')


class CookListView(generic.ListView):
    model = Cook
    template_name = "team.html"
    context_object_name = "cook_list"


def index(request):
    """View function for the home page of the site."""
    print(reverse("meal:meal-create"))
    return render(request, "index.html")


def about(request):
    """View function for the about page of the site."""
    return render(request, "about.html")


def menu(request):
    """View function for the menu page of the site."""
    return render(request, "meal/menu.html")


@login_required()
def booking(request):
    """View function for booking."""
    return render(request, "booking.html")


def contact(request):
    """View function for the contact page of the site."""
    return render(request, "contact.html")
