from django.urls import path
from meal.views import MealListView, MealDetailView, index, about, menu, booking, CookListView, contact, service

urlpatterns = [
    # path("", ),
    path("", index, name="index"),
    path("about/", about, name="about"),
    # path("menu/", menu, name="menu"),
    path("booking/", booking, name="booking"),
    path("team/", CookListView.as_view(), name="team"),
    path("contact/", contact, name="contact"),
    path("service/", service, name="service"),
    path("menu/", MealListView.as_view(), name="menu"),
    path("<slug:slug>/", MealDetailView.as_view(), name="meal-detail"),


]

app_name = "meal"
