from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=User)
def user_pre_save_signal(sender, instance: User, *args, **kwargs):
    instance.email = instance.email.lower()
    instance.username = instance.username.lower()
