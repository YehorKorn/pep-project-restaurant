from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic

from reservation.forms import ReservationForm, ReservationSearchForm
from reservation.models import Reservation


class ReservationCreateView(generic.CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = "reservation/booking.html"
    success_url = reverse_lazy("index")


class ReservationListView(UserPassesTestMixin, generic.ListView):
    model = Reservation
    template_name = "reservation/reservation_list.html"
    context_object_name = "reservation_list"
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ReservationListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = ReservationSearchForm(initial={
            "name": name
        })

        return context

    def get_queryset(self):
        queryset = Reservation.objects.all()
        form = ReservationSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset
