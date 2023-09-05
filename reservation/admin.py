from django.contrib import admin

from reservation.models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    search_fields = ["name, email, phone, date_time"]
    list_filter = ["date_time", "number_of_people"]
