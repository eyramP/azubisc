from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    name = models.CharField(max_length=255)


    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

