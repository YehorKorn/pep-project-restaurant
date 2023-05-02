from django.contrib import admin

from meal.models import Meal


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_filter = ["price", "people", "preparation_time"]
