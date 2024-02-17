from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from author.models import Authors
from books.models import Books

from .models import Reviews


@receiver(pre_save, sender=User)
def user_pre_save_signal(sender, instance: User, *args, **kwargs):
    instance.email = instance.email.lower()
    instance.username = instance.username.lower()


@receiver(post_save, sender=Reviews)
def reviews_post_save_signal(sender, instance: Reviews, created: bool, *args, **kwargs):
    if isinstance(instance.object, Authors):
        ratings = Reviews.objects.filter(
            content_type__app_label='author',
            content_type__model='authors',
            object_id=instance.object.id
        ).values_list('rating', flat=True)
        if ratings.count() != 0:
            author = instance.object
            author.average_rating = sum(ratings)/ratings.count()
            author.save()
    if isinstance(instance.object, Books):
        ratings = Reviews.objects.filter(
            content_type__app_label='books', content_type__model='books',
            object_id=instance.object.id
        ).values_list('rating', flat=True)
        if ratings.count() != 0:
            book = instance.object
            book.average_rating = sum(ratings)/ratings.count()
            book.save()
