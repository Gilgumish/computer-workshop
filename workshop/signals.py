from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Client


@receiver(post_save, sender=User)
def create_client_profile(sender, instance, created, **kwargs):
    if created and instance.is_client:
        Client.objects.create(user=instance)
