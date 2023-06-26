from django.contrib import admin

from reservation.models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    search_fields = ["name, email, phone, date"]
    list_filter = ["date", "number_of_people"]
