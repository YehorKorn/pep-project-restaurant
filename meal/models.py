from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"


class Meal(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=500)
    people = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    preparation_time = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="meals")
    image = models.ImageField(upload_to="meal/")
    slug = models.SlugField(null=True, blank=True, unique=True)

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


class Cook(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    about = models.TextField(max_length=150)
    position = models.CharField(max_length=50)
    image = models.ImageField(upload_to="cooker/")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"


