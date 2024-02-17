from django.db import models

from root.utils.fields import CommonFields

# Create your models here.


class Books(CommonFields):
    title = models.CharField()
    author = models.ForeignKey('author.Authors', on_delete=models.CASCADE)
    average_rating = models.FloatField(default=0)

    class Meta:
        db_table = 'books'
        verbose_name = 'Book'

    def __str__(self) -> str: return self.title
