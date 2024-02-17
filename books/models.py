from django.db import models

from root.utils.fields import CommonFields

# Create your models here.


class Books(CommonFields):
    title = models.CharField()
    author = models.ForeignKey('author.Authors', on_delete=models.CASCADE)

    @property
    def average_rating(self) -> float:
        from main.models import Reviews

        ratings = Reviews.objects.filter(
            content_type__app_label='books', content_type__model='books',
            object_id=self.id
        ).values_list('rating', flat=True)
        if ratings.count() != 0:
            return sum(ratings)/ratings.count()
        return 0

    class Meta:
        db_table = 'books'
        verbose_name = 'Book'

    def __str__(self) -> str: return self.title
