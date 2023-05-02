from django.db import models
from django.utils.text import slugify


class Meal(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    people = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    preparation_time = models.IntegerField()
    image = models.ImageField(upload_to="meal/")
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super(Meal, self).save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )

    def __str__(self):
        return self.name
