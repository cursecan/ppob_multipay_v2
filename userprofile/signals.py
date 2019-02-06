from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import (
    Profile, Wallet
)


@receiver(post_save, sender=User)
def initial_user_profile(sender, instance, created, **kwargs):
    if created:
        profile_obj = Profile.objects.create(
            user = instance, 
            agen = instance
        )

        Wallet.objects.create(
            profile = profile_obj
        )