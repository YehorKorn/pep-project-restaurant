from django.db import models


class Reservation(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.Field()
    date = models.DateField()
    time = models.TimeField()
    number_of_people = models.IntegerField()
    special_request = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
