from django.contrib import admin
from django.urls import path, include
from meal.views import MealListView, MealDetailView

urlpatterns = [
    # path("", ),
    path("", MealListView.as_view(), name="meal-list"),
    path("<slug:slug>/", MealDetailView.as_view(), name="meal-detail"),

]

app_name = "meal"
