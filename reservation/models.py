from django.db import models


class Reservation(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=24)
    date_time = models.DateTimeField(help_text="Date and time when the guest arrives.")
    number_of_people = models.IntegerField()
    special_request = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-date_time"]
