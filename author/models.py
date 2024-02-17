from django.db import models

from root.utils.fields import CommonFields


# Create your models here.
class Authors(CommonFields):
    name = models.CharField()

    @property
    def average_rating(self) -> float:
        from main.models import Reviews

        ratings = Reviews.objects.filter(
            content_type__app_label='author',
            content_type__model='authors',
            object_id=self.id
        ).values_list('rating', flat=True)
        if ratings.count() != 0:
            return sum(ratings)/ratings.count()
        return 0

    class Meta:
        db_table = 'author'
        verbose_name = 'Author'

    def __str__(self) -> str: return self.name
