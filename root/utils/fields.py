from django.db import models

from .utils import slug_generate


class CommonFields(models.Model):
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slug_generate()
        return super().save(*args, **kwargs)
