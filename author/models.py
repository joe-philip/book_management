from django.db import models

from root.utils.fields import CommonFields

# Create your models here.


class Authors(CommonFields):
    name = models.CharField()
    average_rating = models.FloatField(default=0)

    class Meta:
        db_table = 'author'
        verbose_name = 'Author'

    def __str__(self) -> str: return self.name
