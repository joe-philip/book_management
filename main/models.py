from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from root.utils.fields import CommonFields

# Create your models here.


class Reviews(CommonFields):
    class ContentTypeChoices(models.IntegerChoices):
        AUTHOR = (1, 'Author')
        BOOK = (2, 'Book')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey("content_type", "object_id")
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField()

    class Meta:
        db_table = 'reviews'
        verbose_name = 'Review'
        unique_together = ('user', 'content_type', 'object_id')

    def __str__(self) -> str: return f'{self.id}'
