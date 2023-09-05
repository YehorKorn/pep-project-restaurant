from django.contrib import admin

from meal.models import Meal, Category, Cook


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_filter = ["price", "people", "preparation_time"]


admin.site.register(Category)


@admin.register(Cook)
class CookAdmin(admin.ModelAdmin):
    search_fields = ["first_name", "last_name"]
    list_filter = ["position"]
